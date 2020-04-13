#!/usr/bin/python
#######################################################

import liliputien
import liliputienErrors
import pymongo
import unittest
import mongomock


class liliputienTest(unittest.TestCase):
    """unittest for liliputien backend class"""

    def test_databaseConnectionFalse(self):
        """Test database connexion."""
        # pylint: disable=W
        with self.assertRaises(pymongo.errors.ServerSelectionTimeoutError):
            backend = liliputien.liliputien(dbLocator='mongodb://127.1.1.1:1111')
            dbLink = backend.connectDb(200, 200)

    def test_uniqnessOfIdGenerated(self):
        """Test if a subset of generated id are really uniq """
        # pylint: disable=W
        backend = liliputien.liliputien()

        randomListRnd = {}
        countRnd = 0
        for x in range(1, 100000):
            zeIdRnd = backend.getRandomURLId()
            if zeIdRnd in randomListRnd.keys():
                # print("ERROR, key already there for Rnd")
                countRnd += 1
            else:
                randomListRnd[zeIdRnd] = "ok"
        self.assertEqual(countRnd, 0, "No duplicate ID")

    def test_UrlValidation_True(self):
        """Test method when you want add an URL"""
        backend = liliputien.liliputien()
        lstUrl2Validate = ['http://www.google.com/',
                           'https://www.x3rus.com',
                           'http://www.cwi.nl:80/%7Eguido/Python.html',
                           'https://www.linuxfr.org/news/']
        for url in lstUrl2Validate:
            urlIsValid = backend.uriValidator(url)
            self.assertTrue(urlIsValid)

    def test_UrlValidation_False(self):
        """Test method when you want add an URL"""
        backend = liliputien.liliputien()
        lstUrl2Validate = ['http//www.google.com/',
                           'abcdc',
                           '']
        for url in lstUrl2Validate:
            urlIsValid = backend.uriValidator(url)
            self.assertFalse(urlIsValid)

    def test_addUrlRedirection_URL_False(self):
        """Test method when you want add an URL"""
        # pylint: disable=W
        backend = liliputien.liliputien()
        with self.assertRaises(liliputienErrors.urlDontMatchCriteria):
            idURL = backend.addUrlRedirection("www.google.com")

    # def test_getUniqIdFalse(self):
        # need learn mock mongodb + decorate method generateRandomId

    def test_writeLiliURL_True(self):
        """ Test writing operation and check data available """
        backend = liliputien.liliputien()
        # create a fake mongodb collection
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend.writeLiliURL(urlId="Fksi3s", urlTarget="https://www.google.com")
        entryFound = backend.dbCollection.find_one({'short': '/Fksi3s'})
        self.assertIsNotNone(entryFound)

    def test_writeLiliURL_False(self):
        """ Test writing operation and check data available """
        backend = liliputien.liliputien()
        # create a fake mongodb collection
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend.writeLiliURL(urlId="Fksi3s", urlTarget="https://www.google.com")
        entryFound = backend.dbCollection.find_one({'short': '/BaD'})
        self.assertIsNotNone(entryFound)


if __name__ == '__main__':
    unittest.main()
