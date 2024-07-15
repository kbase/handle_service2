import os
import pytest
import requests
import time

from typing import Optional
from lib.AbstractHandle.AbstractHandleClient import AbstractHandle

""" handle_service_container_test.py

Very simple tests to ensure that local handle service server is functioning correctly.
Requires the python libraries `pytest` and `requests` to be installed.

Assumes that the handle_service2 is running locally on ports 8080.

Use the wrapper shell script, `run_tests.sh`, to create the necessary set up and run the tests:

sh scripts/run_tests.sh

"""

# setup TEST_TOKEN as env or provide a TOKEN_FILE_PATH
# export TEST_TOKEN="your-kb-ci-token"
TOKEN_FILE_PATH = None
HANDLE_SERVICE_VERSION = "1.0.7"
FILE_NAME = "mylittlefile"

HS_URL = "http://localhost:8080"
BLOB_URL = "https://ci.kbase.us/services/shock-api"
WAIT_TIMES = [1, 2, 5, 10, 30]


@pytest.fixture(scope="module")
def ready():
    wait_for_hs()

    yield


def wait_for_hs():
    print("waiting for workspace service...")
    hs = AbstractHandle(HS_URL)
    for t in WAIT_TIMES:
        try:
            hs.status()
            return
        except Exception as e:
            print(f"Failed to connect to handle service, waiting {t} sec and trying again:\n\t{e}")
        time.sleep(t)
    raise Exception(f"Couldn't connect to the workspace after {len(WAIT_TIMES)} attempts")


def test_handle_service(ready) -> None:
    """create a node in CI blobstore, and then create and pull the handle"""
    test_hs_version()
    token = get_token(TOKEN_FILE_PATH)
    blob_id = create_node(token)
    create_handle_and_pull(blob_id, token)


def create_handle_and_pull(blod_id: str, token: str) -> None:
    # initial client
    hs = AbstractHandle(HS_URL, token=token)

    # create a handle
    hid = hs.persist_handle(
        {
            "id": blod_id,
            "type": "shock",
            "file_name": FILE_NAME,
            "url": BLOB_URL,
        }
    )
    assert hid[:4] == "KBH_"

    # pull handle
    handles = hs.hids_to_handles([hid])
    assert len(handles) == 1
    handle = handles[0]
    assert handle["hid"] == hid
    assert handle["file_name"] == FILE_NAME
    assert handle["id"] == blod_id


def create_node(token: str) -> str:
    """create a node in CI blobstore"""

    with open(FILE_NAME, 'rb') as file:
        response = requests.post(
            BLOB_URL + "/node",
            headers={
                "content-type":"application/json",
                'Authorization': f'OAuth {token}'
            },
            files={'file': file},
            params={'filename': FILE_NAME, 'format': 'text'}
        )

    assert response.status_code == 200
    node_data = response.json()
    assert "data" in node_data
    return node_data["data"]["id"]


def test_hs_version() -> None:
    """get the current handle service version"""
    hs = AbstractHandle(HS_URL)
    status = hs.status()
    assert status["state"] == "OK"
    assert status["version"] == HANDLE_SERVICE_VERSION


def get_token(token_filepath: Optional[str]) -> str:
    """
    Get the token from the file and then from the env if it's not in the file.
    """
    if token_filepath:
        with open(os.path.expanduser(token_filepath), "r") as f:
            token = f.readline().strip()
    else:
        token = os.environ.get("TEST_TOKEN")
    if not token:
        raise ValueError(
            f"Need to provide a token in the TEST_TOKEN "
            + f"environment variable or as token_filepath argument"
        )
    return token