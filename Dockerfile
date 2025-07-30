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

# Default command: just change this based on what you want to run
CMD ["bash", "-c", "uvicorn  Data-Analysis-Project-02/product/backend/backend:app --host 0.0.0.0 --port 8000 & streamlit run Data-Analysis-Project-02/product/frontend/frontend.py --server.port 8501 --server.address 0.0.0.0"]
