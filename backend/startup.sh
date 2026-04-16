#!/bin/bash

# Install Python packages
pip install -r requirements.txt

# Run gunicorn server
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app.main:app
