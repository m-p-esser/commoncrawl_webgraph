from platform import node, platform

from prefect import flow, get_run_logger


@flow(name="hello_world_flow")
def hello_world_flow():
    """ Hello World Test Flow """
    logger = get_run_logger()
    logger.info("Hello, World!")
    logger.info(f"Running on Network '{node()}' and Instance '{platform()}'")


if __name__ == "__main__":
    hello_world_flow()
