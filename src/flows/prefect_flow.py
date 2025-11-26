import pandas as pd
from prefect import flow, task
import skops.io as sio
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler


@task
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df.drop(columns=["date"])
    return df


@task
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # Precipitation and dew point (columns 2 and 3) should not be imputed with median or scaled.
    # Precipitaion is often zero and dew point is closely related to temperature.
    impute_columns = [
        "relative_humidity_2m",
        "cloud_cover",
        "visibility",
        "wind_gusts_10m",
        "temperature_2m",
    ]

    # Filling missing values
    num_impute = SimpleImputer(strategy="median")

    # Scaling
    scaler = MinMaxScaler()

    df[impute_columns] = num_impute.fit_transform(df[impute_columns])
    df[impute_columns] = scaler.fit_transform(df[impute_columns])
    return df


@task
def data_split(df: pd.DataFrame, target_column: str):
    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=14
    )

    return X_train, X_test, y_train, y_test


@task
def train_model(X_train: pd.DataFrame, y_train: pd.Series):
    model = RandomForestClassifier(n_estimators=100, random_state=14)
    model.fit(X_train, y_train)
    return model


@task
def get_prediction(X_test, model):
    return model.predict(X_test)


@task
def evaluate_model(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", str(round(accuracy, 2) * 100) + "%")
    return accuracy


@task
def save_model(model):
    sio.dump(model, "seeing_model.skops")


@flow(log_prints=True)
def ml_workflow(filename: str = "../data/seeing_weather_data.csv"):
    data = load_data(filename)
    prep_data = process_data(data)
    X_train, X_test, y_train, y_test = data_split(
        prep_data, target_column="seeing_quality"
    )
    model = train_model(X_train, y_train)
    predictions = get_prediction(X_test, model)
    evaluate_model(y_test, predictions)
    save_model(model)


if __name__ == "__main__":
    ml_workflow()
