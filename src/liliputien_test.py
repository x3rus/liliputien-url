#!/usr/bin/python
#######################################################

import unittest
import liliputien
import pymongo


class liliputienTest(unittest.TestCase):
    """unittest for liliputien backend class"""

    def test_databaseConnectionFalse(self):
        """Test database connexion."""
        with self.assertRaises(pymongo.errors.ServerSelectionTimeoutError):
            backend = liliputien.liliputien(dbLocator='mongodb://127.1.1.1:1111')
            dbLink = backend.connectDb(200, 200)


if __name__ == '__main__':
    unittest.main()
