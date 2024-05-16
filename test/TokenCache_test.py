# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from AbstractHandle.Utils.TokenCache import TokenCache

import mongo_util


class TokenCacheTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _, deploy_config = mongo_util.get_config()
        cls.token = deploy_config["test-token"]
        CACHE_EXPIRE_TIME = 300
        cls.token_cache = TokenCache(1000, CACHE_EXPIRE_TIME)

    @classmethod
    def tearDownClass(cls):
        cls.token_cache.clear()
        print('Finished testing TokenCacheUtil')

    def test_token_cache(self):

        # empty token cache at the begining
        self.assertIsNone(self.token_cache.get(self.token))
        self.assertEqual(len(self.token_cache), 0)

        # insert token into cache
        current_time = int(datetime.utcnow().timestamp()*1000)
        token_info = {'customroles': 'test_boss',
                      'expires': current_time + 1000}
        self.token_cache[self.token] = token_info

        # test inserted token info
        self.assertCountEqual(self.token_cache.keys(), [self.token])
        fetched_token_info = self.token_cache.get(self.token)
        self.assertDictEqual(token_info, fetched_token_info)

        # test expired token
        current_time = int(datetime.utcnow().timestamp()*1000)
        token_info = {'customroles': 'test_boss',
                      'expires': current_time - 1000}
        self.token_cache[self.token] = token_info

        self.assertIsNone(self.token_cache.get(self.token))
