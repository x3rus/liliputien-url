#!/usr/bin/python3
#
# Test Client for liliputien cmd
#
########################################

import unittest
# import unittest.mock
from unittest.mock import patch
import client

# TODO the solution I think : https://auth0.com/blog/mocking-api-calls-in-python/#Mocking-a-Whole-Function


class liliputienClientTest(unittest.TestCase):
    """unittest for liliputien client class"""

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    def test_liliputien_client_health_True_check(self):
        """Test method health_check """
        lili = client.liliputienClient("http://127.0.0.1:5000")
        # credit to https://bhch.github.io/posts/2017/09/python-testing-how-to-mock-requests-during-tests/
        with patch('requests.get') as mock_request:
            # return code
            mock_request.return_value.status_code = 200
            # fake content
            mock_request.return_value.content = "Ok"
            result = lili.health_check()
            self.assertEqual(result, True)

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    def test_liliputien_client_health_False_check(self):
        """Test method health_check """
        lili = client.liliputienClient("http://127.0.0.1:5000")
        # credit to https://bhch.github.io/posts/2017/09/python-testing-how-to-mock-requests-during-tests/
        with patch('requests.get') as mock_request:
            # return code
            mock_request.return_value.status_code = 500
            # fake content
            mock_request.return_value.content = "Fake content"
            result = lili.health_check()
            self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
