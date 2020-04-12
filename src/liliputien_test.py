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

    def test_uniqnessOfIdGenerated(self):
        """Test if a subset of generated id are really uniq """
        backend = liliputien.liliputien()

        randomListRnd= {}
        countRnd = 0
        for x in range(1,100000):
            zeIdRnd = backend.getRandomURLId()
            if zeIdRnd in randomListRnd.keys():
                # print("ERROR, key already there for Rnd")
                countRnd += 1
            else:
                randomListRnd[zeIdRnd]="ok"
        self.assertEqual(countRnd,0,"No duplicate ID")


if __name__ == '__main__':
    unittest.main()
