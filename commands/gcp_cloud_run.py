"""Programmatically create Cloud Run block for Prefect"""

from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_run import CloudRunJob

credentials = GcpCredentials.load("commoncrawl-prefect-sa")

project_id = credentials.project

# Artifact Registry in Google Cloud
registry_adress = f"europe-west3-docker.pkg.dev/{project_id}/prefect-flows"

flow_name = "hello-world"

block = CloudRunJob(
    credentials=credentials,
    project_id=project_id,
    image=f"{registry_adress}/{flow_name}:2.10.4-python3.9",
    region="europe-west3",
)

block.save(name="hello-world-cloud-run-block", overwrite=True)
