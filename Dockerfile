FROM python:3.9.7-slim

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt