.PHONY: install-rye format build up

build:
	@if [ -n "`nvidia-smi | grep NVIDIA-SMI`" ]; then \
		echo "NVIDIA GPU detected. Using cuda image for build."; \
		export ARCH="cuda"; \
	else \
		echo "NVIDIA GPU not detected. Using cpu image for build."; \
		export ARCH="cpu"; \
	fi && \
	cp -r src docker/$$ARCH && \
	cp -r view docker/$$ARCH && \
	cp main.py docker/$$ARCH && \
	cp requirements.lock docker/$$ARCH && \
	cp pyproject.toml docker/$$ARCH && \
	cp README.md docker/$$ARCH && \
	cp .env docker/$$ARCH && \
	cd docker/$$ARCH && \
	docker-compose build --no-cache;

up:
	@if [ -n "`nvidia-smi | grep NVIDIA-SMI`" ]; then \
		echo "NVIDIA GPU detected. Using cuda image for build."; \
		export ARCH="cuda"; \
	else \
		echo "NVIDIA GPU not detected. Using cpu image for build."; \
		export ARCH="cpu"; \
	fi && \
	if [ -e "docker/$$ARCH/main.py" ]; then \
		rm -rf docker/$$ARCH/src; \
		rm -rf docker/$$ARCH/view; \
		rm -rf docker/$$ARCH/main.py; \
		rm -rf docker/$$ARCH/requirements.lock; \
		rm -rf docker/$$ARCH/pyproject.toml; \
		rm -rf docker/$$ARCH/README.md; \
		rm -rf docker/$$ARCH/.env; \
	fi && \
	cd docker/$$ARCH && docker-compose up;

install-rye:
	curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
	echo 'source "$$HOME/.rye/env"' >> ~/.bashrc
	source "$$HOME/.rye/env"

format:
	rye run black .
	rye run isort .
	rye run flake8 . --exclude=.venv --max-line-length=88 --ignore=E203,W503
	rye run mypy .
