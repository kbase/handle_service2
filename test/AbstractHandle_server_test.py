# -*- coding: utf-8 -*-
import os
import unittest
import inspect
import copy
import requests as _requests
from unittest.mock import patch
import threading
import queue
from random import randrange
import uuid

from AbstractHandle.AbstractHandleImpl import AbstractHandle
from AbstractHandle.authclient import KBaseAuth as _KBaseAuth
from AbstractHandle.Utils import MongoUtil
from AbstractHandle.Utils.Handler import Handler

import mongo_util
from mongo_controller import MongoController


class handle_serviceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_config, deploy_config = mongo_util.get_config()
        cls.cfg = deploy_config
        cls.token = deploy_config['admin-token']

        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        cls.user_id = auth_client.get_user(cls.token)
        cls.shock_url = cls.cfg['blobstore-url']
        # Normally this is a AbstractHandleserver.MethodContext object. However, due to 10+ year
        # old poor design, on import the server loads the config file and sets up the
        # implementation object, which immediately tries to contact Mongo. We don't need the
        # server for anything else and the context is only used as a simple dictionary in the
        # Impl code and so got rid of the import.
        cls.ctx = {'token': cls.token,
                   'user_id': cls.user_id,
                   'provenance': [
                       {'service': 'AbstractHandle',
                        'method': 'please_never_use_it_in_production',
                        'method_params': []
                       }
                    ],
                    'authenticated': 1
        }

        cls.delete_temp_dir = mongo_config.delete_temp_dir
        cls.mongo_controller = MongoController(
            mongo_config.mongo_exe,
            mongo_config.mongo_temp,
            use_wired_tiger=mongo_config.use_wired_tiger
        )
        cls.cfg['mongo-host'] = "localhost"
        cls.cfg["mongo-port"] = cls.mongo_controller.port
        mongo_util.create_test_db(cls.mongo_controller, db=cls.cfg['mongo-database'])
        cls.serviceImpl = AbstractHandle(cls.cfg)
        cls.mongo_util = MongoUtil.MongoUtil(cls.cfg)
        cls.shock_ids_to_delete = list()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "mongo_controller"):
            cls.mongo_controller.destroy(cls.delete_temp_dir)
        if hasattr(cls, 'shock_ids_to_delete'):
            print('Nodes to delete: {}'.format(cls.shock_ids_to_delete))
            cls.deleteShockID(cls.shock_ids_to_delete)

    @classmethod
    def deleteShockID(cls, shock_ids):
        headers = {'Authorization': 'OAuth {}'.format(cls.token)}
        for shock_id in shock_ids:
            end_point = os.path.join(cls.shock_url, 'node', shock_id)
            resp = _requests.delete(end_point, headers=headers, allow_redirects=True)
            if resp.status_code != 200:
                print('Cannot detele shock node ' + shock_id)
            else:
                print('Deleted shock node ' + shock_id)

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def createTestNode(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        filename = 'mytestfile_{}'.format(str(uuid.uuid4()))
        file_path = os.path.join(curr_dir, filename)

        with open(file_path, 'w') as f:
            f.write('my test file!')

        headers = {'Authorization': 'OAuth {}'.format(self.token)}

        end_point = os.path.join(self.shock_url, 'node?filename={}&format=text'.format(filename))

        with open(file_path, 'rb') as f:
            resp = _requests.post(end_point, data=f, headers=headers)

            if resp.status_code != 200:
                raise ValueError('Grant user readable access failed.\nError Code: {}\n{}\n'
                                 .format(resp.status_code, resp.text))
            else:
                shock_id = resp.json().get('data').get('id')
                self.shock_ids_to_delete.append(shock_id)

        return shock_id

    def start_test(self):
        testname = inspect.stack()[1][3]
        print('\n*** starting test: ' + testname + ' **')

    def test_fetch_handles_by_ok(self):
        self.start_test()
        handler = self.getImpl()

        # test query 'hid' field
        elements = ['KBH_68020', 'KBH_68022', 'KBH_00000']
        field_name = 'hid'
        handles = handler.fetch_handles_by(self.ctx, {'elements': elements, 'field_name': field_name})[0]
        self.assertEqual(len(handles), 2)
        self.assertCountEqual(elements[:2], [h.get('hid') for h in handles])

        # test query 'hid' field with empty data
        elements = ['0']
        field_name = 'hid'
        handles = handler.fetch_handles_by(self.ctx, {'elements': elements, 'field_name': field_name})[0]
        self.assertEqual(len(handles), 0)

        # test query 'id' field
        elements = ['b753774f-0bbd-4b96-9202-89b0c70bf31c']
        field_name = 'id'
        handles = handler.fetch_handles_by(self.ctx, {'elements': elements, 'field_name': field_name})[0]
        self.assertEqual(len(handles), 1)
        handle = handles[0]
        self.assertFalse('_id' in handle)
        self.assertEqual(handle.get('hid'), 'KBH_68020')

    def test_ids_to_handles_ok(self):
        self.start_test()
        handler = self.getImpl()

        ids = ['b753774f-0bbd-4b96-9202-89b0c70bf31c']
        handles = handler.ids_to_handles(self.ctx, ids)[0]
        self.assertEqual(len(handles), 1)
        handle = handles[0]
        self.assertFalse('_id' in handle)
        self.assertEqual(handle.get('hid'), 'KBH_68020')

    def test_hids_to_handles_ok(self):
        self.start_test()
        handler = self.getImpl()

        hids = ['KBH_68020', 'KBH_68022', 'KBH_00000']
        handles = handler.hids_to_handles(self.ctx, hids)[0]
        self.assertEqual(len(handles), 2)
        self.assertCountEqual(hids[:2], [h.get('hid') for h in handles])

    def test_persist_handle_ok(self):
        self.start_test()
        handler = self.getImpl()

        handle = {'id': 'id',
                  'file_name': 'file_name',
                  'type': 'shock',
                  'url': 'http://ci.kbase.us:7044/'}
        # testing persist_handle with non-existing handle (inserting a handle)
        counter = self.mongo_util.get_hid_counter()
        hid = handler.persist_handle(self.ctx, handle)[0]
        new_counter = self.mongo_util.get_hid_counter()
        self.assertEqual(new_counter, counter + 1)
        handles = handler.fetch_handles_by(self.ctx, {'elements': [hid], 'field_name': 'hid'})[0]
        self.assertEqual(len(handles), 1)
        handle_ret = handles[0]
        self.assertEqual(hid, 'KBH_' + str(new_counter))
        self.assertEqual(handle_ret.get('hid'), hid)
        self.assertEqual(handle_ret.get('id'), 'id')
        self.assertEqual(handle_ret.get('file_name'), 'file_name')
        self.assertEqual(handle_ret.get('created_by'), self.user_id)

        # testing persist_handle a second handle
        hid = handler.persist_handle(self.ctx, handle)[0]
        new_counter = self.mongo_util.get_hid_counter()
        self.assertEqual(hid, 'KBH_' + str(new_counter))
        self.assertEqual(new_counter, counter + 2)

        # testing persist_handle with existing handle (should not be allowed)
        new_handle = copy.deepcopy(handle_ret)
        with self.assertRaises(ValueError) as context:
            handler.persist_handle(self.ctx, new_handle)[0]

        self.assertIn('Please do not specify hid', str(context.exception.args))

        self.mongo_util.delete_one(handle)

    def test_persist_multiple_handles_ok(self):
        self.start_test()
        handler = self.getImpl()

        handle = {'id': 'id',
                  'file_name': 'file_name',
                  'type': 'shock',
                  'url': 'http://ci.kbase.us:7044/'}

        counter = self.mongo_util.get_hid_counter()

        thread_count = 257

        threads = list()
        hids = list()
        que = queue.Queue()
        for index in range(thread_count):
            x = threading.Thread(target=lambda q, ctx, handle: q.put(handler.persist_handle(ctx, handle)),
                                 args=(que, self.ctx, handle))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        while not que.empty():
            result = que.get()
            hids.append(int(result[0].split('KBH_')[-1]))

        new_counter = self.mongo_util.get_hid_counter()
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

    def test_delete_handles_ok(self):
        self.start_test()
        handler = self.getImpl()

        handles = [{'id': 'id',
                    'file_name': 'file_name',
                    'type': 'shock',
                    'url': 'http://ci.kbase.us:7044/'}] * 2
        hids_to_delete = list()
        for handle in handles:
            hid = handler.persist_handle(self.ctx, handle)[0]
            hids_to_delete.append(hid)

        handles_to_delete = handler.fetch_handles_by(self.ctx, {'elements': hids_to_delete, 'field_name': 'hid'})[0]

        delete_count = handler.delete_handles(self.ctx, handles_to_delete)[0]

        self.assertEqual(delete_count, len(hids_to_delete))

    def test_is_owner_ok(self):
        self.start_test()
        handler = self.getImpl()

        hids = list()

        node_id = self.createTestNode()
        handle = {'id': node_id,
                  'file_name': 'file_name',
                  'type': 'shock',
                  'url': 'https://ci.kbase.us/services/shock-api'}
        hid = handler.persist_handle(self.ctx, handle)[0]
        hids.append(hid)

        node_id2 = self.createTestNode()
        handle = {'id': node_id2,
                  'file_name': 'file_name',
                  'type': 'Shock',
                  'url': 'https://ci.kbase.us/services/shock-api'}
        hid = handler.persist_handle(self.ctx, handle)[0]
        hids.append(hid)

        is_owner = handler.is_owner(self.ctx, ['FAKEHANDLE_-100'])[0]
        self.assertFalse(is_owner)

        is_owner = handler.is_owner(self.ctx, hids)[0]
        self.assertTrue(is_owner)

        new_handles = handler.fetch_handles_by(self.ctx, {'elements': hids, 'field_name': 'hid'})[0]

        for handle in new_handles:
            self.mongo_util.delete_one(handle)

    def test_are_is_readable_ok(self):

        self.start_test()
        handler = self.getImpl()

        hids = list()

        node_id = self.createTestNode()
        handle = {'id': node_id,
                  'file_name': 'file_name',
                  'type': 'shock',
                  'url': 'https://ci.kbase.us/services/shock-api'}
        hid = handler.persist_handle(self.ctx, handle)[0]
        hids.append(hid)

        node_id = self.createTestNode()
        handle = {'id': node_id,
                  'file_name': 'file_name',
                  'type': 'SHOCK',
                  'url': 'https://ci.kbase.us/services/shock-api'}
        hid = handler.persist_handle(self.ctx, handle)[0]
        hids.append(hid)

        are_readable = handler.are_readable(self.ctx, hids)[0]
        self.assertTrue(are_readable)

        are_readable = handler.are_readable(self.ctx, ['fake_handle_id'])[0]
        self.assertFalse(are_readable)

        is_readable = handler.is_readable(self.ctx, hids[0])[0]
        self.assertTrue(is_readable)

        new_handles = handler.fetch_handles_by(self.ctx, {'elements': hids, 'field_name': 'hid'})[0]

        for handle in new_handles:
            self.mongo_util.delete_one(handle)

    @patch.object(Handler, "_is_admin_user", return_value=True)
    def test_add_read_acl_ok(self, _is_admin_user):
        self.start_test()
        handler = self.getImpl()
        node_id = self.createTestNode()

        hids = list()

        handle = {'id': node_id,
                  'file_name': 'file_name',
                  'type': 'shock',
                  'url': 'https://ci.kbase.us/services/shock-api'}
        hid = handler.persist_handle(self.ctx, handle)[0]
        hids.append(hid)

        headers = {'Authorization': 'OAuth {}'.format(self.token)}
        end_point = os.path.join(self.shock_url, 'node', node_id, 'acl/?verbosity=full')
        resp = _requests.get(end_point, headers=headers)
        data = resp.json()

        # no public access at the beginning
        self.assertFalse(data.get('data').get('public').get('read'))

        # only token user has read access
        users = [user.get('username') for user in data.get('data').get('read')]
        self.assertCountEqual(users, [self.user_id])

        # grant public read access
        succeed = handler.set_public_read(self.ctx, hids)[0]
        self.assertTrue(succeed)
        resp = _requests.get(end_point, headers=headers)
        data = resp.json()
        self.assertTrue(data.get('data').get('public').get('read'))

        # should work for already publicly accessable ndoes
        succeed = handler.set_public_read(self.ctx, hids)[0]
        self.assertTrue(succeed)
        resp = _requests.get(end_point, headers=headers)
        data = resp.json()
        self.assertTrue(data.get('data').get('public').get('read'))

        # test grant access to user who already has read access
        succeed = handler.add_read_acl(self.ctx, hids, username=self.user_id)[0]
        self.assertTrue(succeed)
        resp = _requests.get(end_point, headers=headers)
        data = resp.json()
        new_users = [user.get('username') for user in data.get('data').get('read')]
        self.assertCountEqual(new_users, [self.user_id])

        # grant access to kbasetest
        new_user = 'kbasetest'
        succeed = handler.add_read_acl(self.ctx, hids, username=new_user)[0]
        self.assertTrue(succeed)
        resp = _requests.get(end_point, headers=headers)
        data = resp.json()
        new_users = [user.get('username') for user in data.get('data').get('read')]
        self.assertCountEqual(new_users, [self.user_id, new_user])

        handles_to_delete = handler.fetch_handles_by(self.ctx, {'elements': hids, 'field_name': 'hid'})[0]
        delete_count = handler.delete_handles(self.ctx, handles_to_delete)[0]
        self.assertEqual(delete_count, len(hids))
