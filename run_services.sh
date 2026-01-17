#!/bin/bash

# Start local FastAPI server (background)
echo "Starting API Server..."
uvicorn app.api.server:app --host 0.0.0.0 --port 8000 &

# Start Streamlit app (background)
echo "Starting Streamlit App..."
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
