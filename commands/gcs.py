""" Programmatically create GCS block for Prefect"""

from prefect.filesystems import GCS

with open("credentials/service_account.json", "r") as f:
    service_account = f.read()

block = GCS(
    bucket_path="common_crawl_bucket/",
    service_account_info=service_account,
    project="commoncrawl-383811",
)

block.save("commoncrawl-bucket")
