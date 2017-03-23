import proxy_checker
import unittest


class TestProxy(unittest.TestCase):
    def test_check(self):
        worker = proxy_checker.MyThread('http://122.228.179.178:80')
        worker.run()
