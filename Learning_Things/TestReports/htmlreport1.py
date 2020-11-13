'''
Created on Aug 19, 2018
@author: zhaosong
'''

import unittest
import HtmlTestRunner

class MyTestExample(unittest.TestCase):
    '''
    This class demo how to setup test case and run test use python unittest module.
    '''

    # This method will be executed only once for this test case class.
    # It will execute before all test methods. Must decorated with @classmethod.
    @classmethod
    def setUpClass(cls):
        pass

    # Similar with setupClass method, it will be executed after all test method run.
    @classmethod
    def tearDownClass(cls):
        pass

    # This method will be executed before each test function.
    def setUp(self):
        pass

    # This method will be executed after each test function.
    def tearDown(self):
        pass

    def test_function_one(self):
        print("test_function_one execute.")
        self.assertEqual(1, 1, "test_function_one.")

    def test_function_two(self):
        print("test_function_two execute.")
        self.assertNotEqual(1, 2, "test_function_two.")

    def test_function_three(self):
        print("test_function_three execute.")

    def test_function_four(self):
        print("test_function_four execute.")



