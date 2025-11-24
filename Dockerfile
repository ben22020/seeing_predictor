FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Default workdir contains your code
COPY . .

CMD ["python", "-m", "src.utils.discord_bot"]