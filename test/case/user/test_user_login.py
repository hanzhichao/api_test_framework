import unittest
from test.case.basecase import BaseCase


class TestUserLogin(BaseCase):
    def test_user_login_normal(self):
        """level1:正常登录"""
        case_data = self.get_case_data("test_user_login_normal")
        self.send_request(case_data)

    def test_user_login_password_wrong(self):
        """密码错误登录"""
        case_data = self.get_case_data("test_user_login_password_wrong")
        self.send_request(case_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # t = TestUserLogin()
    # print(t.test_user_login_normal().__tags__)
    # suite = unittest.TestSuite()
    # suite.addTest(TestUserLogin('test_user_login_normal'))
    # for i in suite:
    #     print(i)

    # unittest.TextTestRunner().run(suite)
