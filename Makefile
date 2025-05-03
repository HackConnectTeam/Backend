PROJECT_NAME?=$(shell awk '/^\[project\]/ {flag=1; next} /^\[/ {flag=0} flag && /^name = / {print}' pyproject.toml | sed -n 's/^name = "\([^"]*\)"/\1/p')
IS_ROOTLESS?=$(shell docker info -f "{{println .SecurityOptions}}" | grep rootless > /dev/null 2>&1 && echo 1 || echo 0)

UV_VERSION ?= 0.5.14
UV_IMAGE ?= ghcr.io/astral-sh/uv:$(UV_VERSION)
PROJECT_PATH := $(shell pwd)

build:
	docker build \
        -t $(PROJECT_NAME) \
        -f devops/Dockerfile \
        .
shell:
	docker run --rm -it \
		--name $(PROJECT_NAME)-$(STAGE)-container \
		--network host \
		--gpus all \
		--shm-size=7g \
		-e PYTHONPATH=/opt/project \
		-v $(shell pwd):/opt/project \
		-v /.root/cache:/root/.cache \
		$(PROJECT_NAME) bash


build-deps:
	docker build \
		-t uv-with-shell \
		-f devops/deps.Dockerfile \
		.

run-deps:
	docker run --rm -it \
		-v $(shell pwd):/opt/project \
		-e IS_ROOTLESS=$(IS_ROOTLESS) \
		uv-with-shell

deps: build-deps run-deps
