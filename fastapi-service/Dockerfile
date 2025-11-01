FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files
COPY proto/ ./proto/

# Copy application code
COPY app/ ./app/

# Generate Python gRPC code from proto files into app directory
RUN python -m grpc_tools.protoc -I proto --python_out=app --grpc_python_out=app proto/currency.proto

EXPOSE 50051

CMD ["python", "app/grpc_server.py"]

