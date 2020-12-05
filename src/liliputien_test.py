#!/usr/bin/python
#######################################################

import liliputien
import liliputienErrors
import datetime
import unittest
import mongomock
# import pymongo


class liliputienTest(unittest.TestCase):
    """unittest for liliputien backend class"""

# TODO : need fix
#    def test_databaseConnectionFalse(self):
#        """Test database connexion."""
#        # pylint: disable=W
#        # with self.assertRaises(pymongo.errors.ServerSelectionTimeoutError):
#        backend = liliputien.liliputien(dbLocator='mongodb://127.1.6.1:2111')
#        dbLink = backend.connectDb(200, 200)
#        self.assertIsNone(dbLink)

    def test_uniqnessOfIdGenerated(self):
        """Test if a subset of generated id are really uniq """
        # pylint: disable=W
        backend = liliputien.liliputien()

        randomListRnd = {}
        countRnd = 0
        for x in range(1, 100000):
            zeIdRnd = backend._getRandomURLId()
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
            urlIsValid = backend._uriValidator(url)
            self.assertTrue(urlIsValid)

    def test_UrlValidation_False(self):
        """Test method when you want add an URL"""
        backend = liliputien.liliputien()
        lstUrl2Validate = ['http//www.google.com/',
                           'abcdc',
                           '']
        for url in lstUrl2Validate:
            urlIsValid = backend._uriValidator(url)
            self.assertFalse(urlIsValid)

    def test_addUrlRedirection_URL_False(self):
        """Test method when you want add an URL"""
        # pylint: disable=W
        backend = liliputien.liliputien()
        with self.assertRaises(liliputienErrors.urlDontMatchCriteria):
            backend.addUrlRedirection("www.google.com")

    def test_getUrlRedirection_Exception(self):
        """Test method to get url destination base on url ID """
        backend = liliputien.liliputien()
        backend.dbCollection = mongomock.MongoClient().db.collection
        with self.assertRaises(liliputienErrors.urlIdNotFound):
            backend.getUrlRedirection('/aaaaaa')

    def test_getUrlRedirection_True(self):
        """Test method to get url destination base on url ID """
        backend = liliputien.liliputien()
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend.dbCollection = AddFewEntryInMockedMongoDb(backend.dbCollection)

        entryFound = backend.getUrlRedirection('/QQa83d')
        self.assertEqual(entryFound, "https://www.lequipe.fr/Football")

    def test_getUrlRedirection_FalseMultiple(self):
        """Test method to get url destination base on url ID """
        # pylint: disable=W
        backend = liliputien.liliputien()
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend.dbCollection = AddFewEntryInMockedMongoDb(backend.dbCollection)

        # Add duplicate entry
        dbEntry = {"short": "/QQa83d",
                   "urlDst": "https://tube.lesamarien.fr/videos/trending?a-state=42",
                   "date": datetime.datetime.utcnow()
                   }
        backend.dbCollection.insert_one(dbEntry).inserted_id

        with self.assertRaises(liliputienErrors.urlIdMultipleOccurenceFound):
            backend.getUrlRedirection(urlId='/QQa83d', strict=True)

    def test_getUrlRedirection_TrueMultiple(self):
        """Test method to get url destination base on url ID """
        # pylint: disable=W
        backend = liliputien.liliputien()
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend.dbCollection = AddFewEntryInMockedMongoDb(backend.dbCollection)

        # Add duplicate entry
        dbEntry = {"short": "/QQa83d",
                   "urlDst": "https://tube.lesamarien.fr/videos/trending?a-state=42",
                   "date": datetime.datetime.utcnow()
                   }
        backend.dbCollection.insert_one(dbEntry).inserted_id

        entryFound = backend.getUrlRedirection(urlId='/QQa83d')
        self.assertEqual(entryFound, "https://www.lequipe.fr/Football")

    # def test_getUniqIdFalse(self):
        # need learn mock mongodb + decorate method generateRandomId

    def test_writeLiliURL_True(self):
        """ Test writing operation and check data available """
        backend = liliputien.liliputien()
        # create a fake mongodb collection
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend._writeLiliURL(urlId="/Fksi3a", urlTarget="https://www.google.com")
        entryFound = backend.dbCollection.find_one({'short': '/Fksi3a'})
        self.assertIsNotNone(entryFound)

    def test_writeLiliURL_False(self):
        """ Test writing operation and check data available """
        backend = liliputien.liliputien()
        # create a fake mongodb collection
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend._writeLiliURL(urlId="Fksi3s", urlTarget="https://www.google.com")
        entryFound = backend.dbCollection.find_one({'short': '/BaD'})
        self.assertIsNone(entryFound)

    def test_List_Urls_True(self):
        """Test method when you want retrieve all URLs"""
        backend = liliputien.liliputien()
        backend.dbCollection = mongomock.MongoClient().db.collection
        backend.dbCollection = AddFewEntryInMockedMongoDb(backend.dbCollection)
        urls = backend.getUrls()
        self.assertEqual(urls[0]['urlDst'], "http://www.google.com")
        self.assertEqual(urls[1]['short'], "/sE8c2D")


def AddFewEntryInMockedMongoDb(collection):
    """ Add few entry in the database and return collection """
    dbEntry = {"short": "/Dk8c3",
               "urlDst": "http://www.google.com",
               "date": datetime.datetime.utcnow()
               }
    collection.insert_one(dbEntry).inserted_id

    dbEntry = {"short": "/sE8c2D",
               "urlDst": "https://www.linuxfr.org",
               "date": datetime.datetime.utcnow()
               }
    collection.insert_one(dbEntry).inserted_id

    dbEntry = {"short": "/QQa83d",
               "urlDst": "https://www.lequipe.fr/Football",
               "date": datetime.datetime.utcnow()
               }
    collection.insert_one(dbEntry).inserted_id
    return collection


if __name__ == '__main__':
    unittest.main()
