import logging
import os
from typing import List, Tuple
from configparser import ConfigParser
from datetime import datetime
from mongo_controller import MongoController
from AbstractHandle.Utils import MongoUtil

# Mongo config
TEST_CONFIG_PATH = "HANDLE_SERVICE_TEST_CFG"
TEST_SECTION = "HandleService2"
TEST_MONGO_EXE = "test.mongo.exe"
TEST_TEMP_DIR = "test.temp.dir"
TEST_USE_WIRED_TIGER = "test.mongo.wired_tiger"
TEST_DELETE_TEMP_DIR = "test.delete.temp.dir"

# Deploy config
TEST_AUTH_SERVICE_URL = "auth-service-url"
TEST_AUTH_URL = "auth-url"
TEST_SHOCK_URL = "shock-url"
TEST_ADMIN_TOKEN = "admin-token"
TEST_ADMIN_ROLES = "admin-roles"
TEST_NAME_SPACE = "namespace"

def get_config() -> Tuple[List[str], dict[str, str]]:
    """
    Returns:
        Mongo config that stores mongo executable, temporary directory, wired_tiger, and delete_temp_dir
        Deploy config that stores auther_serice_url, auth_url, shock_url, admin_token, admin_roles, and namespace
    """
    config_path = _get_config_file_path()
    section = _get_test_config(config_path)

    mongo_exe_path = _get_value(section, TEST_MONGO_EXE, config_path, True)
    mongo_temp_dir = _get_value(section, TEST_TEMP_DIR, config_path, True)
    wired_tiger = _get_value(section, TEST_USE_WIRED_TIGER, config_path, False)
    delete_temp_dir = _get_value(section, TEST_DELETE_TEMP_DIR, config_path, False)

    auth_serivce_url = _get_value(section, TEST_AUTH_SERVICE_URL, config_path, True)
    auth_url = _get_value(section, TEST_AUTH_URL, config_path, True)
    shock_url = _get_value(section, TEST_SHOCK_URL, config_path, True)
    admin_token = _get_value(section, TEST_ADMIN_TOKEN, config_path, True)
    admin_roles = _get_value(section, TEST_ADMIN_ROLES, config_path, True)
    name_space = _get_value(section, TEST_NAME_SPACE, config_path, True)

    mongo_config = [
        mongo_exe_path,
        mongo_temp_dir,
        wired_tiger=="true",
        delete_temp_dir!="false",
    ]

    deploy_config = {
        TEST_AUTH_SERVICE_URL: auth_serivce_url,
        TEST_AUTH_URL: auth_url,
        TEST_SHOCK_URL: shock_url,
        TEST_ADMIN_TOKEN: admin_token,
        TEST_ADMIN_ROLES: admin_roles,
        TEST_NAME_SPACE: name_space,
    }

    return mongo_config, deploy_config

def _get_config_file_path() -> str:
    config_path = os.environ.get(TEST_CONFIG_PATH)
    if not config_path:
        raise ValueError(
            f"Must supply absolute path to test config file in {TEST_CONFIG_PATH} environment variable"
        )
    return config_path

def _get_test_config(config_path) -> dict[str, str]:
    cfg = dict()
    config = ConfigParser()
    config.read(config_path)
    for key, val in config.items(TEST_SECTION):
        cfg[key] = val
    return config

def _get_value(section, key, path, required) -> str:
    val = section.get(key, "").strip()
    if val == "" and required:
        raise ValueError(
            f"Required key {key} in section {TEST_SECTION} in config file {path} is missing a value"
		)
    return val

def _get_default_handles():

    raw_handles = [
        [68020, 'b753774f-0bbd-4b96-9202-89b0c70bf31c', 'interleaved.fastq', 'shock', 'http://ci.kbase.us:7044/', None, None, 'tgu2', datetime.utcnow()],
        [68021, '4cb26117-9793-4354-98a6-926c02a7bd0e', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', '2c40e80ae4fb981541fc6918035c8707', None, 'tgu2', datetime.utcnow()],
        [68022, 'cadf4bd8-7d95-4edd-994c-b50e29c25e50', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', 'e47f6adcaa33436ad0746fe9f936e359', None, 'tgu2', datetime.utcnow()],
        [68023, 'd24188ed-83ff-4939-9dc2-84cc758738a3', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', '1da5481d162ca923c3ad27722ffdd377', None, 'tgu2', datetime.utcnow()],
        [68024, 'acd1d64b-da98-467f-b29c-baca2862dd23', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', '43966480eabf5848fdc6046ba4214bee', None, 'tgu2', datetime.utcnow()],
        [68025, 'f973cbd3-8881-4281-afef-a8419629e813', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', 'c374414a78a20feb716ea71c0ecf0a58', None, 'tgu2', datetime.utcnow()],
        [68026, 'a676f82a-adc5-478e-b85a-d8244eae965e', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', '79cc52fff3c465681d162ce3caa6e672', None, 'tgu2', datetime.utcnow()],
        [68027, 'f4113d56-9840-4811-b32d-4ae09523389a', 'SP1.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', '15aa9c1535b0da2158f169c748ee2a11', None, 'tgu2', datetime.utcnow()],
        [68028, 'a31db49f-447c-4fff-96d5-2981166c0b9b', 'tmp_fastq.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', 'f78e79df067806daa1f0946ddc790b53', None, 'tgu2', datetime.utcnow()],
        [68029, '7a2ff7c8-d87d-4c25-ad25-5f85ea794afa', 'tmp_fastq.fq.gz', 'shock', 'https://ci.kbase.us/services/shock-api', '05361e0506af15be6701b175adbb23e4', None, 'tgu2', datetime.utcnow()]]

    key_names = ['_id', 'hid', 'id', 'file_name', 'type', 'url', 'remote_md5', 'remote_sha1',
                 'created_by', 'creation_date']

    handles = list()
    for handle in raw_handles:
        handle_doc = dict()
        handle_doc.update({key_names[0]: int(handle[0])})
        for idx, h in enumerate(handle):
            handle_doc.update({key_names[idx + 1]: h})

        handles.append(handle_doc)

    return handles

def create_test_db(
    mc: MongoController,
    db='handle_db',
    col=MongoUtil.MONGO_COLLECTION,
    hid_col=MongoUtil.MONGO_HID_COUNTER_COLLECTION
):

    logging.info('creating collection and dbs')

    my_client = mc.client
    my_db = my_client[db]
    my_collection = my_db[col]
    my_hid_collection = my_db[hid_col]

    handles = _get_default_handles()

    my_collection.delete_many({})
    my_hid_collection.delete_many({})

    my_collection.insert_many(handles)
    my_hid_collection.insert_one({'_id': 'hid_counter', 'hid_counter': 68030})

    logging.info('created db: {}'.format(my_client.list_database_names()))

