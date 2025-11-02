# Set base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install Python dependencies
# 將 dependencies 和 code 分開 COPY，可以利用 Docker 的 layer cache，減少重建映像檔的時間
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Set environment variable
ENV FLASK_ENV=production

# Set entrypoint
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8000"]
