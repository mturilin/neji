"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.http import HttpRequest

from django.test import TestCase
from neji.python_lang import validate_python_code
from neji.views import runpython


class SimpleTest(TestCase):

    def __test_runpython(self):
        request = HttpRequest()

        request.POST["python_code"] = "for i in range(10):\n\tprint i"
        request.method = "POST"

        response = runpython(request)
        print response.content

        self.assertEqual(response.content, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n")


    def test_validate_strings(self):
        python_code = """print 'Hello, world!'

import math

from os.blabla import koko

print math.exp(1)

print os.listdir("/")


print "bla bla bla '''' \" " """

        self.assertEquals(['Import from module "os" is not allowed. Check Python page for explanation.'],
            validate_python_code(python_code))


    def test_validate_split_lines(self):
        python_code = """
print 'Hello, world!'

import \\
    os

print os.listdir("/")
"""

        self.assertEquals(['Import from module "os" is not allowed. Check Python page for explanation.'],
            validate_python_code(python_code))


    def test_validate_split_lines_with_comma(self):
        python_code = """
print 'Hello, world!'

import \\
    math, os

print os.listdir("/")
"""

        self.assertEquals(['Import from module "os" is not allowed. Check Python page for explanation.'],
            validate_python_code(python_code))


