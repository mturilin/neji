"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.http import HttpRequest

from django.test import TestCase
from neji.views import runpython


class SimpleTest(TestCase):

    def test_runpython(self):
        request = HttpRequest()

        request.POST["python_code"] = "for i in range(10):\n\tprint i"
        request.method = "POST"

        response = runpython(request)
        print response.content

        self.assertEqual(response.content, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n")


