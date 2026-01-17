FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
# 8501 for Streamlit
# 8000 for FastAPI (WhatsApp Bot)
EXPOSE 8501
EXPOSE 8000

# Copy start script and make executable
COPY run_services.sh .
RUN chmod +x run_services.sh

# Start services
CMD ["./run_services.sh"]
