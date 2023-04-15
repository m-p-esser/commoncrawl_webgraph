from prefect import get_client
from prefect.deployments import Deployment
from prefect.filesystems import GCS
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_run import CloudRunJob

from src.flows.hello_world import hello_world_flow

client = get_client()

# Load Blocks
credentials = GcpCredentials.load("commoncrawl-prefect-sa")
storage = GCS.load("commoncrawl-bucket")
cloud_run_block = CloudRunJob.load("hello-world-cloud-run-block")

deployment = Deployment.build_from_flow(
    flow=hello_world_flow,
    name="hello-world-deployment",
    storage=storage,
    infrastructure=cloud_run_block,
)

if __name__ == "__main__":
    deployment.apply()
