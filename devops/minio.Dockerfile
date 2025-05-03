# Use the official MinIO image
FROM minio/minio:latest

# Expose the MinIO API port (default: 9000)
EXPOSE 9000

# Start the MinIO server with default data path and enable the web console on port 9001
CMD ["server", "/data", "--console-address", ":9001"]
