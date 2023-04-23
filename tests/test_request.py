""" Module to test the functions in the request submodule """

import pytest

from src.commoncrawl import request


@pytest.fixture
def example_index_file_response():
    index_table_path_gz = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-14/cc-index-table.paths.gz"

    response = request.request_file(index_table_path_gz)

    return response


# Happy Path - Requesting Response containing Index File Bytes suceeds
def test_request_file_succeeds(example_index_file_response):
    assert example_index_file_response.status_code == 200
    assert example_index_file_response.headers["Content-Type"] == "binary/octet-stream"


# Failed Path - URL Reference lies in future
def test_request_file_fails_future_url():
    index_table_path_gz = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2100-14/cc-index-table.paths.gz"

    response = request.request_file(index_table_path_gz)

    assert response.status_code == 404


# Failed Path - URL Reference is not gz.paths file
def test_request_file_fails_no_gz_path():
    with pytest.raises(ValueError):
        index_table_path_gz = (
            "https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-14/cc-index-table"
        )

        request.request_file(index_table_path_gz)


# Happy Path - Getting Index File List succeeds
def test_get_index_files_succeeds(example_index_file_response):
    bytes_buffer = request.hexadecimal_to_buffer(example_index_file_response)
    index_files = request.get_file_list_from_gz_buffer(bytes_buffer)

    assert len(index_files) > 0
    assert (
        index_files[0]
        == "cc-index/table/cc-main/warc/crawl=CC-MAIN-2023-14/subset=crawldiagnostics/part-00000-39c03058-7d78-443d-9984-102329513e3d.c000.gz.parquet"
    )
