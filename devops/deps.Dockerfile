# Use a base Python image with a slim version to minimize the image size
FROM python:3.12-slim

# Set up the home directory (just for clarity, adjust as needed)
ARG HOME=/home/root

# Set environment variables to add virtual environment and local bin to PATH
ENV PATH="$HOME/.local/bin:${VIRTUAL_ENV}/bin:$PATH"
ENV UV_LINK_MODE=copy

# Install bash, curl, and git (to ensure you have bash for shell access and git for version control)
RUN apt-get update && \
    apt-get install -y curl bash git && \
    rm -rf /var/lib/apt/lists/*

# Install 'uv' using pip (reliable way to install uv as a Python package)
RUN pip install uv

# Set the working directory to /project where your project code will be mounted
WORKDIR /opt/project

# Set entry point to bash so you can interact with the container
ENTRYPOINT ["bash"]
