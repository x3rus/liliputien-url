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


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:5000/health':
        return MockResponse(None, 200)
    elif args[0] == 'http://unhealty.url.com:5000/health':
        return MockResponse(None, 500)

    return MockResponse(None, 404)


class liliputienClientTest(unittest.TestCase):
    """unittest for liliputien client class"""

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    def test_liliputien_client_health_check(self):
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

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
#    @unittest.mock.patch('requests.get', side_effect=mocked_requests_get)
#    def test_liliputien_client_bad_health_check(self):
#        """Test method health_check """
#        lili = client.liliputienClient('http://unhealty.url.com:5000/health')
#        result = lili.health_check()
#        self.assertEqual(result, 500)


if __name__ == "__main__":
    unittest.main()
