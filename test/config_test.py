import os
import unittest

from pathlib import Path

import mongo_util
from test_helper import create_temp_file
from AbstractHandle.Utils.MongoUtil import MongoUtil


DEFAULT_TEST_CONFIG_PATH = os.environ[mongo_util.TEST_CONFIG_ENV_PATH]


class ConfigTest(unittest.TestCase):

    def test_minimal_config(self):
        data_string = """[HandleService2]\n
        test.mongo.exe=mongod\n
        test.temp.dir=temp_test_dir\n
        auth-service-url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login\n
        auth-url=https://ci.kbase.us/services/auth\n
        shock-url=https://ci.kbase.us/services/shock-api\n
        admin-token=998\n
        test-token=999\n
        admin-roles=HANDLE_ADMIN, KBASE_ADMIN\n
        namespace=KBH\n
        mongo-database=handle_db
        """
        try:
            cfg_path = create_temp_file(data_string)
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = cfg_path
            mongo_cfg, deploy_cfg = mongo_util.get_config()
        finally:
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = DEFAULT_TEST_CONFIG_PATH

        # check mongo config
        self.assertEqual(mongo_cfg.mongo_exe, Path("mongod"))
        self.assertEqual(mongo_cfg.mongo_temp, Path("temp_test_dir"))
        self.assertEqual(mongo_cfg.use_wired_tiger, False)
        self.assertEqual(mongo_cfg.delete_temp_dir, True)

        # check deploy config
        self.assertEqual(
            deploy_cfg["auth-service-url"],
            "https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login",
        )
        self.assertEqual(deploy_cfg["auth-url"], "https://ci.kbase.us/services/auth")
        self.assertEqual(
            deploy_cfg["shock-url"], "https://ci.kbase.us/services/shock-api"
        )
        self.assertEqual(deploy_cfg["admin-token"], "998")
        self.assertEqual(deploy_cfg["test-token"], "999")
        self.assertEqual(deploy_cfg["admin-roles"], "HANDLE_ADMIN, KBASE_ADMIN")
        self.assertEqual(deploy_cfg["namespace"], "KBH")
        self.assertEqual(deploy_cfg["mongo-database"], "handle_db")
        self.assertEqual(deploy_cfg["mongo-user"], "")
        self.assertEqual(deploy_cfg["mongo-password"], "")
        self.assertEqual(deploy_cfg["mongo-retrywrites"], "")

        # make a config and pass it into MongoUtil
        cfg = deploy_cfg
        cfg["mongo-host"] = "localhost"
        cfg["mongo-port"] = 8888
        cfg["mongo-authmechanism"] = "DEFAULT"
        mu = MongoUtil(cfg)

        # assert on the instance variables
        self.assertEqual(mu.mongo_host, "localhost")
        self.assertEqual(mu.mongo_port, 8888)
        self.assertEqual(mu.mongo_database, "handle_db")
        self.assertEqual(mu.mongo_user, "")
        self.assertEqual(mu.mongo_pass, "")
        self.assertEqual(mu.mongo_authmechanism, "DEFAULT")
        self.assertEqual(mu.mongo_retrywrites, False)

        # remove temp file
        os.remove(cfg_path)

    def test_maximal_config(self):
        data_string = """[HandleService2]\n
        test.mongo.exe=mongod\n
        test.temp.dir=temp_test_dir\n
        test.mongo.wired_tiger=true\n
        test.delete.temp.dir=false\n
        auth-service-url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login\n
        auth-url=https://ci.kbase.us/services/auth\n
        shock-url=https://ci.kbase.us/services/shock-api\n
        admin-token=998\n
        test-token=999\n
        admin-roles=HANDLE_ADMIN, KBASE_ADMIN\n
        namespace=KBH\n
        mongo-database=handle_db\n
        mongo-user=mongouser\n
        mongo-password=mongopassword\n
        mongo-retrywrites=true
        """
        try:
            cfg_path = create_temp_file(data_string)
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = cfg_path
            mongo_cfg, deploy_cfg = mongo_util.get_config()
        finally:
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = DEFAULT_TEST_CONFIG_PATH

        # check mongo config
        self.assertEqual(mongo_cfg.mongo_exe, Path("mongod"))
        self.assertEqual(mongo_cfg.mongo_temp, Path("temp_test_dir"))
        self.assertEqual(mongo_cfg.use_wired_tiger, True)
        self.assertEqual(mongo_cfg.delete_temp_dir, False)

        # check deploy config
        self.assertEqual(
            deploy_cfg["auth-service-url"],
            "https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login",
        )
        self.assertEqual(deploy_cfg["auth-url"], "https://ci.kbase.us/services/auth")
        self.assertEqual(
            deploy_cfg["shock-url"], "https://ci.kbase.us/services/shock-api"
        )
        self.assertEqual(deploy_cfg["admin-token"], "998")
        self.assertEqual(deploy_cfg["test-token"], "999")
        self.assertEqual(deploy_cfg["admin-roles"], "HANDLE_ADMIN, KBASE_ADMIN")
        self.assertEqual(deploy_cfg["namespace"], "KBH")
        self.assertEqual(deploy_cfg["mongo-database"], "handle_db")
        self.assertEqual(deploy_cfg["mongo-user"], "mongouser")
        self.assertEqual(deploy_cfg["mongo-password"], "mongopassword")
        self.assertEqual(deploy_cfg["mongo-retrywrites"], "true")

        # make a config and pass it into MongoUtil
        cfg = deploy_cfg
        cfg["mongo-host"] = "localhost"
        cfg["mongo-port"] = 8888
        cfg["mongo-authmechanism"] = "DEFAULT"
        mu = MongoUtil(cfg)

        # assert on the instance variables
        self.assertEqual(mu.mongo_host, "localhost")
        self.assertEqual(mu.mongo_port, 8888)
        self.assertEqual(mu.mongo_database, "handle_db")
        self.assertEqual(mu.mongo_user, "mongouser")
        self.assertEqual(mu.mongo_pass, "mongopassword")
        self.assertEqual(mu.mongo_authmechanism, "DEFAULT")
        self.assertEqual(mu.mongo_retrywrites, True)

        # remove temp file
        os.remove(cfg_path)
