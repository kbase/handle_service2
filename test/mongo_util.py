import logging
import os
import uuid
from pathlib import Path
from typing import Tuple
from datetime import datetime
from mongo_controller import MongoController
from AbstractHandle.Utils import MongoUtil

MONGO_EXE_PATH="MONGO_EXE_PATH"
MONGO_TEMP_DIR="MONGO_TEMP_DIR"


def get_mongo_info() -> Tuple[Path, Path]:
    """
    Returns a tuple of
    * The path to the mongo executable from the environment
    * the path to a root directory for temporary mongo data from the environment.
    """
    return (Path(os.environ.get(MONGO_EXE_PATH)), Path(os.environ.get(MONGO_TEMP_DIR)))


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

