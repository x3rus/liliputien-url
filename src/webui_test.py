#!/usr/bin/python
#######################################################

import unittest
from webui import app


class liliputienWebTest(unittest.TestCase):
    """unittest for liliputien webui class"""

    # executed prior to each test
    def setUp(self):
        app.config['SECRET_KEY'] = 'Ze-test-key-not-secure'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    # tests

    def test_homepage_True(self):
        """Test home page."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome at Liliputien URL', response.data)

    def test_homepage_False(self):
        """Test home page."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Not in the Page', response.data)
    
if __name__ == "__main__":
    unittest.main()
