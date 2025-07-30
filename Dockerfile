# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Streamlit (8501) and FastAPI (8000) ports
EXPOSE 8501
EXPOSE 8000

# Default command: start backend and wait until it's ready before launching frontend
CMD ["bash", "-c", "\
uvicorn Data-Analysis-Project-02/product/backend/backend:app --host 0.0.0.0 --port 8000 & \
echo 'Waiting for backend to start...'; \
until curl -s http://127.0.0.1:8000/docs > /dev/null; do \
    sleep 1; \
done; \
echo 'Backend is up. Starting frontend...'; \
streamlit run Data-Analysis-Project-02/product/frontend/frontend.py --server.port 8501 --server.address 0.0.0.0"]

