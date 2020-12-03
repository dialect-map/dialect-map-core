APP_VERSION    = $(shell cat VERSION)
IMAGE_NAME     = "dialect-map-server"

COV_CONFIG     = ".coveragerc"
SOURCE_FOLDER  = "src"
TESTS_FOLDER   = "tests"
TESTS_PARAMS   = "-p no:cacheprovider"
TYPING_PARAMS  = "--allow-redefinition --ignore-missing-imports --cache-dir=/dev/null"

GCP_PROJECT   ?= "ds3-dialect-map"
GCP_REGISTRY  ?= "us.gcr.io"
GCP_IMAGE_NAME = $(GCP_REGISTRY)/$(GCP_PROJECT)/$(IMAGE_NAME)


.PHONY: build
build:
	@echo "Building Docker image"
	@docker build . \
		--tag $(IMAGE_NAME):$(APP_VERSION) \
		--tag $(IMAGE_NAME):latest


.PHONY: check
check:
	@echo "Checking code format"
	@black --check $(SOURCE_FOLDER)
	@black --check $(TESTS_FOLDER)
	@echo "Checking type annotations"
	@mypy "$(TYPING_PARAMS)" $(SOURCE_FOLDER)
	@mypy "$(TYPING_PARAMS)" $(TESTS_FOLDER)


.PHONY: install-dev
install-dev:
	@echo "Installing Development packages"
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt
	@pre-commit install


.PHONY: push
push: build
	@echo "Pushing Docker image to GCP"
	@docker tag $(IMAGE_NAME):$(APP_VERSION) $(GCP_IMAGE_NAME):$(APP_VERSION)
	@docker push $(GCP_IMAGE_NAME):$(APP_VERSION)
	@docker rmi $(GCP_IMAGE_NAME):$(APP_VERSION)


.PHONY: test
test:
	@echo "Testing code"
	@pytest --cov-config=$(COV_CONFIG) --cov=$(SOURCE_FOLDER) "$(TESTS_PARAMS)"
