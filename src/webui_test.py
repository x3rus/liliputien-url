#!/usr/bin/python
#######################################################

import unittest
from webui import app, _get_dict_from_flashed_messages, backend
import mongomock


class liliputienWebTest(unittest.TestCase):
    """unittest for liliputien webui class"""

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    # tests

    # TODO : merge test with table test
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

    def test_add_True(self):
        """Test home page."""
        response = self.app.get('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'urlTarget', response.data)

    def test_add_form_True(self):
        """Test add form without enter url target """
        backend.dbCollection = mongomock.MongoClient().db.collection
        response = self.app.post('/add', data=dict(
                                  urlTarget="http://www.google.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.data)
        self.assertIn(b'Your link is added', response.data)

    def test_add_form_False(self):
        """Test add form without enter url target """
        backend.dbCollection = mongomock.MongoClient().db.collection
        response = self.app.post('/add', data=dict(
                                  urlTarget="not_a_valide_url"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.data)
        self.assertIn(b'Oupss', response.data)

    def test_get_dict_from_flashed_messages_True(self):
        flashedMessageOriginal = ['targetUrl ; http://www.google.com', 'otherInfo ; bonjour']

        dictFlashedMsg = _get_dict_from_flashed_messages(flashedMessageOriginal)
        self.assertEqual(dictFlashedMsg['targetUrl'],'http://www.google.com')

if __name__ == "__main__":
    unittest.main()
