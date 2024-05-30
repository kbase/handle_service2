import os
import tempfile
import unittest

from pathlib import Path

import mongo_util


class ConfigTest(unittest.TestCase):

    def test_minimal_config(self):
        data_string = """[HandleService2]\n
        test.mongo.exe=mongod\n
        test.temp.dir=temp_test_dir\n
        auth-service-url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login\n
        auth-url=https://ci.kbase.us/services/auth\n
        shock-url=https://ci.kbase.us/services/shock-api\n
        admin-token=998\n
        test-token=998\n
        admin-roles=HANDLE_ADMIN, KBASE_ADMIN\n
        namespace=KBH\n
        mongo-database=handle_db\n
        mongo-retrywrites=false
        """
        try:
            cfg_path = self._create_temp_file(data_string)
            default_path = os.environ[mongo_util.TEST_CONFIG_ENV_PATH]
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = cfg_path
            mongo_cfg, deploy_cfg = mongo_util.get_config()
        finally:
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = default_path

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
        self.assertEqual(deploy_cfg["test-token"], "998")
        self.assertEqual(deploy_cfg["admin-roles"], "HANDLE_ADMIN, KBASE_ADMIN")
        self.assertEqual(deploy_cfg["namespace"], "KBH")
        self.assertEqual(deploy_cfg["mongo-database"], "handle_db")
        self.assertEqual(deploy_cfg["mongo-user"], "")
        self.assertEqual(deploy_cfg["mongo-password"], "")
        self.assertEqual(deploy_cfg["mongo-retrywrites"], False)

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
        test-token=998\n
        admin-roles=HANDLE_ADMIN, KBASE_ADMIN\n
        namespace=KBH\n
        mongo-database=handle_db\n
        mongo-user=mongouser\n
        mongo-password=mongopassword\n
        mongo-retrywrites=true
        """
        try:
            cfg_path = self._create_temp_file(data_string)
            default_path = os.environ[mongo_util.TEST_CONFIG_ENV_PATH]
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = cfg_path
            mongo_cfg, deploy_cfg = mongo_util.get_config()
        finally:
            os.environ[mongo_util.TEST_CONFIG_ENV_PATH] = default_path

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
        self.assertEqual(deploy_cfg["test-token"], "998")
        self.assertEqual(deploy_cfg["admin-roles"], "HANDLE_ADMIN, KBASE_ADMIN")
        self.assertEqual(deploy_cfg["namespace"], "KBH")
        self.assertEqual(deploy_cfg["mongo-database"], "handle_db")
        self.assertEqual(deploy_cfg["mongo-user"], "mongouser")
        self.assertEqual(deploy_cfg["mongo-password"], "mongopassword")
        self.assertEqual(deploy_cfg["mongo-retrywrites"], True)

        # remove temp file
        os.remove(cfg_path)

    def _create_temp_file(data_string):
        try:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
                temp_file.write(data_string)
                file_path = temp_file.name
            return file_path

        except Exception as e:
            raise ValueError("An error occurred:") from e
