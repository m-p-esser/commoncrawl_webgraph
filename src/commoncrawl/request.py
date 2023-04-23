""" Module to request data from the Common Crawl server """

import gzip
from io import BytesIO

import requests


def is_paths_gz_url(url: str) -> bool:
    """Check if the url is pointing to a paths.gz file"""
    if url.endswith("paths.gz"):
        return True
    else:
        return False


def request_file(url: str) -> requests.Response:
    """Request a file

    Args:
        url (str): The url to a paths.gz file

    Returns:
        response (requests.Response): The response of the file
    """

    if is_paths_gz_url(url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

        except requests.exceptions.HTTPError as error:
            print(f"HTTP error occurred: {error}")

        except requests.exceptions.ConnectionError as error:
            print(f"Connection error occurred: {error}")

        except requests.exceptions.Timeout as error:
            print(f"Timeout error occurred: {error}")

        except requests.exceptions.RequestException as error:
            print(f"An error occurred: {error}")

    else:
        raise ValueError(
            f"The url ('{url}') provided is not a paths.gz file. Please use a url that ends with paths.gz"
        )

    return response


def hexadecimal_to_buffer(response: requests.Response) -> BytesIO:
    """Convert a hexadecimal byte string to a buffer

    Args:
        response (requests.Response): The response of the file

    Returns:
        bytes_buffer (BytesIO): The buffer of the file
    """

    bytes_hexadecimal = response.content
    bytes_buffer = BytesIO(bytes_hexadecimal)

    return bytes_buffer


def get_file_list_from_gz_buffer(bytes_buffer: BytesIO) -> list[str]:
    """Get a file list from a buffer

    Args:
        bytes_buffer (BytesIO): The buffer containing the .gz file

    Returns:
        file_list (list[str]): A list of files (that need to be appended to the base url)
    """

    f = gzip.GzipFile(fileobj=bytes_buffer)
    file_list = f.read().decode().splitlines()

    return file_list


# def get_wat_files_data(wat_url: str, extract_length: int = 10000) -> str:
#     """Download the WAT files from WAT url

#     Args:
#         wat_url (str): The url of the WAT file

#     Returns:
#         wat_files_data (str): A string of the WAT file

#     """

#     response = requests.get(wat_url)

#     # Decompress the file
#     bytes = response.content
#     bytes_buffer = BytesIO(bytes)
#     f = gzip.GzipFile(fileobj=bytes_buffer)

#     # Load multiple WAT files as a string
#     wat_files_data = f.read().decode()

#     # Extract only the first N characters
#     wat_files_data = wat_files_data[:extract_length]

#     return wat_files_data
