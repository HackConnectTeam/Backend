FROM quay.io/minio/minio:latest

# The command to run MinIO, with API on port 9005 and the WebUI on port 9006
CMD ["minio", "server", "/data", "--address", "0.0.0.0:9000", "--console-address", ":9090"]
