import os
import pickle
import logging
from time import time

from lib.HTMLTestReportCN import HTMLTestRunner
from config import config
from lib.send_email import send_email
from test.suite.test_suites import *


def discover():
    return unittest.defaultTestLoader.discover(config.test_case_path)


def save_failures(result, file):
    suite = unittest.TestSuite()
    for case_result in result.failures:
        suite.addTest(case_result[0])

    with open(file, 'wb') as f:
        pickle.dump(suite, f)


def collect():
    suite = unittest.TestSuite()

    def _collect(tests):
        if isinstance(tests, unittest.TestSuite):
            if tests.countTestCases() != 0:
                for i in tests:
                    _collect(i)
        else:
            suite.addTest(tests)

    _collect(discover())
    return suite


def makesuite_by_testlist(testlist_file):

    with open(testlist_file) as f:
        testlist = f.readlines()

    testlist = [i.strip() for i in testlist if not i.startswith("#")]

    suite = unittest.TestSuite()
    all_cases = collect()
    for case in all_cases:
        if case._testMethodName in testlist:
            suite.addTest(case)
    return suite


def makesuite_by_tag(tag):
    suite = unittest.TestSuite()
    for case in collect():
        if case._testMethodDoc and tag in case._testMethodDoc:
            suite.addTest(case)

    return suite


def run(suite):
    seps = '='*25
    logging.info(f"{seps} 测试开始 {seps}")

    with open(config.report_file, 'wb') as f:  # 从配置文件中读取
        result = HTMLTestRunner(stream=f, title="Api Test", description="测试描述", tester="韩志超", verbosity=3).run(suite)

    if result.failures:
        if not os.path.exists(config.cache_dir):
            os.makedirs(config.cache_dir)
        save_failures(result, config.last_fails_file)

    if config.send_email_after_run:
        send_email(config.report_file)  # 从配置文件中读取
    logging.info(f"{seps} 测试结束 {seps}")


def collect_only():
    t0 = time.time()
    i = 0
    for case in collect():
        i += 1
        print("{}.{}".format(str(i), case.id()))
    print("-" * 100)
    print("Collect {} tests is {:.3f}s".format(str(i), time.time()-t0))


def run_all():
    run(discover())


def run_suite(suite_name):
    suite = get_suite(suite_name)
    if isinstance(suite, unittest.TestSuite):
        run(suite)
    else:
        print("TestSuite不存在")


def run_by_testlist():
    run(makesuite_by_testlist(config.testlist_file))


def run_by_tag(tag):
    run(makesuite_by_tag(tag))


def rerun_fails():
    sys.path.append(config.test_case_path)
    with open(config.last_fails_file, 'rb') as f:
        suite = pickle.load(f)
    run(suite)


def main():
    options = config.options
    if options.collect_only:
        collect_only()
    elif options.rerun_fails:
        rerun_fails()
    elif options.testlist:
        run(makesuite_by_testlist(config.testlist_file))
    elif options.testsuite:
        run_suite(options.testsuite)
    elif options.tag:
        run(makesuite_by_tag(options.tag))
    else:
        run_all()


if __name__ == '__main__':
    main()
