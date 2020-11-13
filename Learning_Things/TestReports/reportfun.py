import unittest
import HtmlTestRunner
from htmlTestReports.htmlreport1 import MyTestExample

html_report_dir="D:\Selenium\Python\Reports"



#     # Run all test functions with HtmlTestRunner to generate html test report.
def run_all_test_generate_html_report():
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='D:\Selenium\Python\Reports'))



# #Run specified test functions in test suite.
# def run_test_suite(test_function_name):
#     test_suite=unittest.TestSuite()
#     test_suite.addTest(MyTestExample(test_function_name))
#     test_result=unittest.TestResult()
#     test_suite.run(test_result)
#     print(test_result)

# # Run specified test functions and generate html test report.
# def run_test_suite_generate_html_report(test_function_name):
#     # Create a TestSuite object.
#     test_suite = unittest.TestSuite()
#
#     # Add test function in the suite.
#     test_suite.addTest(MyTestExample(test_function_name))
#
#     # Create HtmlTestRunner object and run the test suite.
#     test_runner = HtmlTestRunner.HTMLTestRunner(output=html_report_dir)
#     test_runner.run(test_suite)
#

# # Run all test functions in the specified test case class, the function parameter must be a class name not the class name string.
# def run_all_test_in_class(test_case_class):
#     # Create a TestSuite object.
#     test_suite = unittest.TestSuite()
#
#     # Make all test function
#     test = unittest.makeSuite(test_case_class)
#     test_suite.addTest(test)
#
#     # Create a test result and run the test suite.
#     testResult = unittest.TestResult()
#     test_suite.run(testResult)
#     print(testResult)


# Run all test functions in the specified test case class, the function parameter must be a class name not the class name string.
# def run_all_test_in_class_generate_html_report(test_case_class):
#
#     # Create a TestSuite object.
#     test_suite = unittest.TestSuite()
#
#     # Make all test function
#     test = unittest.makeSuite(test_case_class)
#     test_suite.addTest(test)
#
#     # Create HtmlTestRunner object and run the test suite.
#     test_runner = HtmlTestRunner.HTMLTestRunner(output=html_report_dir)
#     test_runner.run(test_suite)
if __name__ == '__main__':
    run_all_test_generate_html_report()
#     # Run all test functions.
#     # run_test_suite('test_function_three')
#     #run_test_suite_generate_html_report('test_function_three')
#     #run_all_test_in_class(MyTestExample)
#     run_all_test_in_class_generate_html_report(MyTestExample)
