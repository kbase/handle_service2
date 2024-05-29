# -*- coding: utf-8 -*-
import os
import unittest
import inspect
import copy
import threading
import queue
from random import randrange

from AbstractHandle.Utils.MongoUtil import MongoUtil

import mongo_util
from mongo_controller import MongoController
from test_helper import get_hid_counter


# TODO switch all tests to pytest, see sample_service for an example


class MongoUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_config, deploy_config = mongo_util.get_config()
        cls.cfg = deploy_config
        cls.cfg['mongo-authmechanism'] = 'DEFAULT'

        cls.delete_temp_dir = mongo_config.delete_temp_dir
        cls.mongo_controller = MongoController(
            mongo_config.mongo_exe,
            mongo_config.mongo_temp,
            use_wired_tiger=mongo_config.use_wired_tiger
        )
        cls.cfg['mongo-host'] = "localhost"
        cls.cfg["mongo-port"] = cls.mongo_controller.port
        mongo_util.create_test_db(cls.mongo_controller, db=cls.cfg['mongo-database'])
        cls.mongo_util = MongoUtil(cls.cfg)
        cls.hid_counter_collection = cls.mongo_util.hid_counter_collection

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "mongo_controller"):
            cls.mongo_controller.destroy(cls.delete_temp_dir)
        print('Finished testing MongoUtil')

    def getMongoUtil(self):
        return self.__class__.mongo_util

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def test_get_collection(self):
        self.start_test()
        mongo_util = self.getMongoUtil()
        with self.assertRaises(ValueError) as context:
            mongo_util._get_collection('fake_mongo_host', 1234, 'mongo_database', 'mongo_collection')

        self.assertIn('Connot connect to Mongo server', str(context.exception.args))

    def test_init_ok(self):
        self.start_test()
        class_attri = [
            'mongo_host', 'mongo_port', 'mongo_database', 'handle_collection', 
            'hid_counter_collection',
        ]
        mongo_util = self.getMongoUtil()
        self.assertTrue(set(class_attri) <= set(mongo_util.__dict__.keys()))

        handle_collection = mongo_util.handle_collection
        self.assertEqual(handle_collection.name, 'handle')
        self.assertEqual(handle_collection.count_documents({}), 10)

        handle_col_info = handle_collection.index_information()
        handle_col_idx = handle_col_info.keys()
        expected_idx = ['_id_', 'hid_1']
        self.assertEqual(list(handle_col_idx), expected_idx)
        self.assertTrue(handle_col_info['hid_1']['unique'])

        hid_counter_collection = mongo_util.hid_counter_collection
        self.assertEqual(hid_counter_collection.name, 'handle_id_counter')

    def test_find_in_ok(self):
        self.start_test()
        mongo_util = self.getMongoUtil()

        # test query 'hid' field
        elements = [68020, 68022, 0]
        docs = mongo_util.find_in(elements, 'hid')
        self.assertEqual(len(list(docs)), 2)

        # test query 'hid' field with empty data
        elements = [0]
        docs = mongo_util.find_in(elements, 'hid')
        self.assertEqual(len(list(docs)), 0)

        # test query 'id' field
        elements = ['b753774f-0bbd-4b96-9202-89b0c70bf31c']
        docs = mongo_util.find_in(elements, 'id')
        self.assertEqual(len(list(docs.clone())), 1)
        doc = docs.next()
        self.assertFalse('_id' in doc.keys())
        self.assertEqual(doc.get('hid'), 68020)

        # test null projection
        elements = ['b753774f-0bbd-4b96-9202-89b0c70bf31c']
        docs = mongo_util.find_in(elements, 'id', projection=None)
        self.assertEqual(len(list(docs.clone())), 1)
        doc = docs.next()
        self.assertEqual(doc.get('_id'), 68020)
        self.assertEqual(doc.get('hid'), 68020)

    def test_update_one_ok(self):
        self.start_test()
        mongo_util = self.getMongoUtil()

        elements = ['b753774f-0bbd-4b96-9202-89b0c70bf31c']
        docs = mongo_util.find_in(elements, 'id', projection=None)
        self.assertEqual(len(list(docs.clone())), 1)
        doc = docs.next()
        self.assertEqual(doc.get('created_by'), 'tgu2')

        update_doc = copy.deepcopy(doc)
        new_user = 'test_user'
        update_doc['created_by'] = new_user

        mongo_util.update_one(update_doc)

        docs = mongo_util.find_in(elements, 'id', projection=None)
        new_doc = docs.next()
        self.assertEqual(new_doc.get('created_by'), new_user)

        mongo_util.update_one(doc)

    def test_insert_one_ok(self):
        self.start_test()
        mongo_util = self.getMongoUtil()
        self.assertEqual(mongo_util.handle_collection.count_documents({}), 10)

        doc = {'_id': 9999, 'hid': 9999, 'file_name': 'fake_file'}
        counter = get_hid_counter(self.hid_counter_collection)
        mongo_util.insert_one(doc)
        new_counter = get_hid_counter(self.hid_counter_collection)
        self.assertEqual(new_counter, counter)

        self.assertEqual(mongo_util.handle_collection.count_documents({}), 11)
        elements = [9999]
        docs = mongo_util.find_in(elements, 'hid', projection=None)
        self.assertEqual(len(list(docs.clone())), 1)
        doc = docs.next()
        self.assertEqual(doc.get('hid'), 9999)
        self.assertEqual(doc.get('file_name'), 'fake_file')

        mongo_util.delete_one(doc)
        self.assertEqual(mongo_util.handle_collection.count_documents({}), 10)

    def test_increase_counter_with_multi_threads(self):

        mongo_util = self.getMongoUtil()
        counter = get_hid_counter(self.hid_counter_collection)

        thread_count = 329

        threads = list()
        hids = list()
        que = queue.Queue()
        for index in range(thread_count):
            x = threading.Thread(target=que.put(mongo_util.increase_counter()))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        while not que.empty():
            hids.append(que.get())

        new_counter = get_hid_counter(self.hid_counter_collection)
        self.assertEqual(counter + thread_count, new_counter)

        self.assertEqual(len(set(hids)), thread_count)
        self.assertEqual(len(hids), len(set(hids)))

        hids.sort()
        self.assertEqual(hids[0], counter + 1)
        self.assertEqual(hids[-1], new_counter)

        rand_pos = randrange(thread_count)
        self.assertEqual(hids[rand_pos], counter + 1 + rand_pos)

        rand_pos = randrange(thread_count)
        self.assertEqual(hids[-rand_pos], new_counter + 1 - rand_pos)

    def test_delete_one_ok(self):
        self.start_test()
        mongo_util = self.getMongoUtil()
        docs = mongo_util.handle_collection.find()
        self.assertEqual(len(list(docs.clone())), 10)

        doc = docs.next()
        hid = doc.get('hid')
        mongo_util.delete_one(doc)
        self.assertEqual(mongo_util.handle_collection.count_documents({}), 9)

        docs = mongo_util.find_in([hid], 'hid', projection=None)
        self.assertEqual(len(list(docs)), 0)

        mongo_util.insert_one(doc)
        self.assertEqual(mongo_util.handle_collection.count_documents({}), 10)
        docs = mongo_util.find_in([hid], 'hid', projection=None)
        self.assertEqual(len(list(docs)), 1)

    def test_delete_many_ok(self):
        self.start_test()
        mongo_util = self.getMongoUtil()
        docs = mongo_util.handle_collection.find()
        self.assertEqual(len(list(docs.clone())), 10)

        docs_to_delete = list()
        docs_to_delete.append(docs.next())
        docs_to_delete.append(docs.next())
        docs_to_delete = docs_to_delete * 2  # test delete duplicate items
        deleted_count = mongo_util.delete_many(docs_to_delete)
        self.assertEqual(deleted_count, 2)
        self.assertEqual(mongo_util.handle_collection.count_documents({}), 8)
        docs = mongo_util.find_in([doc.get('hid') for doc in docs_to_delete], 'hid')
        self.assertEqual(len(list(docs)), 0)

        for doc in docs_to_delete:
            try:
                mongo_util.insert_one(doc)
            except Exception:
                pass
        self.assertEqual(mongo_util.handle_collection.count_documents({}), 10)
        docs = mongo_util.find_in([doc.get('hid') for doc in docs_to_delete], 'hid')
        self.assertEqual(len(list(docs)), 2)
