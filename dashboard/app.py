from flask import Flask, request, render_template
import os
import sys
sys.path.append("..")
import unittest
import pickle
# from config.config import *


app2 = Flask(__name__)

case_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test', 'case')



def discover():
    return unittest.defaultTestLoader.discover(case_path)


def save(result, file):
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

@app2.route("/", methods=["GET"])
def index():
    cases = []
    for case in collect():
        cases.append(case.id())
    return render_template("list.html", cases=cases)


def get_suite_detail():
    pass



if __name__ == "__main__":
    app2.run(port=5002)