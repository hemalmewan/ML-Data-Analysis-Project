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

# Expose Streamlit (8502) and FastAPI (8001) ports
EXPOSE 8502
EXPOSE 8001

# Default command: start backend and wait until it's ready before launching frontend
CMD ["bash", "-c", "uvicorn backend.backend:app --host 0.0.0.0 --port 8001 & streamlit run main.py --server.port 8502 --server.address 0.0.0.0"]

