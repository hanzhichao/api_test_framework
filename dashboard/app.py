from flask import Flask, request, render_template, redirect
import os
import sys
sys.path.append("..")
import unittest
import pickle
from lib.HTMLTestReportCN import HTMLTestRunner


app = Flask(__name__)


app_dir = os.path.dirname(os.path.abspath(__file__))
case_dir = os.path.join(os.path.dirname(app_dir), 'test', 'case')
suite_dir = os.path.join(app_dir, 'suites')

report_file = os.path.join(app_dir, 'templates','report.html')

def discover():
    return unittest.defaultTestLoader.discover(case_dir)


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


@app.route("/", methods=['GET', 'POST'])
def suite_list():
    suite_list = [suite.split(".")[0] for suite in os.listdir('suites') if suite.endswith(".testsuite")]
    if request.method == 'POST':
        suite_name = request.form.get("suite")
        sys.path.append(case_dir)
        with open(os.path.join(suite_dir, suite_name+".testsuite"), 'rb') as f:
            suite = pickle.load(f)

        with open(report_file, 'wb') as f:  # 从配置文件中读取
            result = HTMLTestRunner(stream=f, title="Api Test", description="测试描述", tester="卡卡").run(suite)
        return redirect("/report")

    return render_template('suite_list.html', suite_list=suite_list)



@app.route("/suite_add", methods=["GET", "POST"])
def suite_add():
    tests = []

    for case in collect():
        tests.append(case.id())

    if request.method == "POST":
        suite_name = request.form.get("suite_name")
        cases = request.form.getlist("cases")
        suite = unittest.defaultTestLoader.loadTestsFromNames(cases)

        with open(os.path.join(suite_dir, suite_name+".testsuite"), 'wb') as f:
            pickle.dump(suite, f)

        return redirect("/list")
        # unittest.TextTestRunner(verbosity=2).run(suite)

    return render_template('suite_add.html', tests=tests)



@app.route("/report", methods=['GET', 'POST'])
def report():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(port="5005", debug=True)