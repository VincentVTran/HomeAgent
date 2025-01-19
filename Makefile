SHELL := /bin/bash

# Define variables
ENV_FILE = .env
OLLAMA_DEPLOYMENT_FILE = ./k8-deployments/ollama-deployment.yaml
# Load environment variables from .env file
ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    export $(shell sed 's/=.*//' $(ENV_FILE))
endif

# Deploy application
deploy:
	envsubst < $(OLLAMA_DEPLOYMENT_FILE) | kubectl apply -f -