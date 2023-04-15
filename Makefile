##################### Initializing | needs run once at project start

# Initializing Git
initialize_git:
	@echo "Initializing git..."
	git init

# Installing Poetry
install: 
	@echo "Installing..."
	poetry install

activate_precommit:
	poetry run pre-commit install

# Install the package from the root project directory for easier developing
# install_package:
# 	@echo "Installing package..."
# 	pip install -e .

# enable required GCP services
enable_gcp_services:
	@echo "Enabling GCP services..."
	gcloud services enable iamcredentials.googleapis.com
	gcloud services enable artifactregistry.googleapis.com
	gcloud services enable run.googleapis.com
	gcloud services enable compute.googleapis.com

# Create Service accounts and add policies
create_gcp_sa:
	@echo "Creating GCP service account..."
	load_env
	gcloud iam service-accounts create $GCP_SA_NAME
	export MEMBER=serviceAccount:"$GCP_SA_NAME"@"$CLOUDSDK_CORE_PROJECT".iam.gserviceaccount.com
	gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/run.admin"
	gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/compute.instanceAdmin.v1"
	gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/artifactregistry.admin"
	gcloud projects add-iam-policy-binding $CLOUDSDK_CORE_PROJECT --member=$MEMBER --role="roles/iam.serviceAccountUser"

# Create Service Account Keyfile
create_gcp_sa_keyfile:
	@echo "Creating GCP service account keyfile..."
	gcloud iam service-accounts keys create prefect.json --iam-account="$GCP_SA_NAME"@"$CLOUDSDK_CORE_PROJECT".iam.gserviceaccount.com

##################### Startup | needs run everytime you open the Command line

# Activate Virtual Env
activate:
	@echo "Activating virtual environment"
	poetry shell

# Load Env variables
load_env:
	@echo "Loading environment variables"
	export CLOUDSDK_CORE_PROJECT="commoncrawl-383811"
	export CLOUDSDK_COMPUTE_REGION=europe-west3
	export GCP_AR_REPO=placeholder
	export GCP_SA_NAME=prefect-sa


##################### Testing functions | needs to run before committing new functions

test:
	pytest

##################### Deployment

export_dependencies:
	poetry export -o "requirements.txt" --without-hashes --without-urls

build_docker_image:
	docker build -t europe-west3-docker.pkg.dev/commoncrawl-383811/prefect-flows/hello-world-flow:2.10.4-python3.9 .
	gcloud auth configure-docker europe-west3-docker.pkg.dev
	docker push europe-west3-docker.pkg.dev/commoncrawl-383811/prefect-flows/hello-world-flow:2.10.4-python3.9



##################### Documentation

docs_view:
	@echo View API documentation... 
	PYTHONPATH=src pdoc src --http localhost:8080

docs_save:
	@echo Save documentation to docs... 
	PYTHONPATH=src pdoc src -o docs

##################### Clean up

# Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache