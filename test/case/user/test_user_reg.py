import unittest
from test.case.basecase import BaseCase
from lib.db import *
import json


class TestUserReg(BaseCase):

    def test_user_reg_normal(self):
        case_data = self.get_case_data("test_user_reg_normal")

        # 环境检查
        name = json.loads(case_data.get("args")).get('name')  # 范冰冰
        if check_user(name):
            del_user(name)
        # 发送请求
        self.send_request(case_data)
        # 数据库断言
        self.assertTrue(check_user(name))
        # 环境清理
        del_user(name)

    def test_user_reg_exist(self):
        case_data = self.get_case_data("test_user_reg_exist")

        name = json.loads(case_data.get("args")).get('name')
        # 环境检查
        if not check_user(name):
            add_user(name, '123456')

        # 发送请求
        self.send_request(case_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)  # 运行所有用例
