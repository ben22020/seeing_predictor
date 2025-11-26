from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/ben22020/prefect.git",
        entrypoint="prefect_tutorial.py:ml_workflow",
    ).deploy(
        name="first-prefect-deployment",
        work_pool_name="default-work-pool",
        tags=["dev"],
        job_variables={"pip_packages": ["pandas", "skops", "scikit-learn"]},
    )
