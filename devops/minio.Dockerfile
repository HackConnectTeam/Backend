FROM quay.io/minio/minio:latest

EXPOSE 9005 9006

# The command to run MinIO, with API on port 9005 and the WebUI on port 9006
CMD ["minio", "server", "/data", "--address", ":9005", "--console-address", ":9006"]
