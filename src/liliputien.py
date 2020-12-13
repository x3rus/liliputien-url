#!/usr/bin/python3
#
#####################################

import datetime
import liliputienErrors
import pymongo
import random
import string
import urllib.parse       # for mongodb password
from urllib.parse import urlparse


class liliputien():
    """backend class, store urls and business logic"""
    def __init__(self, dbLocator='mongodb://%s:%s@localhost:27017/', databaseName="liliputien",
                 collection="dbUrl", user="", passwd="", idSize=6):
        """Init liliputien"""
        self.databaseName = databaseName
        self.dbLocator = dbLocator
        self.dbCollection = None
        self.collection = collection
        self.idSize = idSize
        self.passwd = urllib.parse.quote_plus(passwd)
        self.user = urllib.parse.quote_plus(user)

    def connectDb(self, connectTimeoutMS=20000, serverSelectionTimeoutMS=30000):
        """Establish the DB connection.
        Args : connectTimeoutMS = 20000 (20 sec)
        """
        if self.user != "" and self.passwd != "":
            mongoSrv = pymongo.MongoClient(self.dbLocator % (self.user, self.passwd),
                                           connectTimeoutMS=connectTimeoutMS,
                                           serverSelectionTimeoutMS=serverSelectionTimeoutMS)
        else:
            mongoSrv = pymongo.MongoClient(self.dbLocator, connectTimeoutMS=connectTimeoutMS,
                                           serverSelectionTimeoutMS=serverSelectionTimeoutMS)

        # Select DB  / create it
        liliDb = mongoSrv[self.databaseName]
        self.dbCollection = liliDb.dbUrl                 # TODO check to use self.collection intend of dbUrl
        return self.dbCollection

    def addUrlRedirection(self, urlDestination, shortUrl=None):
        """add an entry in mongodb, validate the entry
            return : dictionnary with url info
            raise : liliputienErrors.urlDontMatchCriteria
        """

        if not self._uriValidator(urlDestination):
            raise liliputienErrors.urlDontMatchCriteria

        if shortUrl is not None:
            if self.dbCollection.find_one({'short': shortUrl}):
                raise liliputienErrors.urlIdMultipleOccurenceFound
            else:
                urlId = self._getUniqUrlId()
        else:
            urlId = self._getUniqUrlId()
            if urlId is None:
                raise liliputienErrors.unableGettingUniqUrlID

        MongoEntry = self._writeLiliURL(urlId, urlDestination)
        if MongoEntry is None:
            raise liliputienErrors.unableWritingUrlEntry

        return urlId, MongoEntry

    def getUrlRedirection(self, urlId, strict=False):
        """ retrieve from database the entry for urlId
            return: target Url
        """

        countUrlId = self.dbCollection.count_documents({"short": urlId})
        lstUrlFound = self.dbCollection.find({"short": urlId})

        if countUrlId > 1 and strict is True:
            raise liliputienErrors.urlIdMultipleOccurenceFound

        if countUrlId == 0:
            raise liliputienErrors.urlIdNotFound

        return lstUrlFound[0]['urlDst']

    def getUrls(self, strict=False):
        """ retrieve all url from database
            return: table of dictionnary
        """

        return list(self.dbCollection.find())

    def updateUrls(self, urlId, urlDstUpdate=None, newDate=None):
        """ update url information
            param: urlId short url to be able change information
                   urlDstUpdate New url destination
                   newDate new date datetime.datetime
            return: url entry from mongo
        """
        countUrlId = self.dbCollection.count_documents({"short": urlId})

        if countUrlId == 0:
            raise liliputienErrors.urlIdMultipleOccurenceFound

        if urlDstUpdate is not None:
            self.dbCollection.update_one({"short": urlId}, {"$set": {"urlDst": urlDstUpdate}})

        if newDate is not None:
            self.dbCollection.update_one({"short": urlId}, {"$set": {"date": newDate}})

        return self.dbCollection.find_one({"short": urlId})

    def getUrl(self, short_url, strict=False):
        """ retrieve one url from database base one the short_url
            param : string short_url
            return: table of dictionnary
        """

        return list(self.dbCollection.find({"short": short_url}))

    def _getRandomURLId(self, size=None, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        """ Generate the random ID /fk8dS3 """
        if size is None:
            size = self.idSize
        return ''.join(random.choice(chars) for _ in range(size))

    def _getUniqUrlId(self, size=None, maxRetry=3):
        """ Return Url ID uniq validat with the DB """
        if size is None:
            size = self.idSize

        idUniq = False
        returnedId = None
        count = 0
        # check if it's already in the DB
        while idUniq is False and count <= maxRetry:
            count += 1
            id = self._getRandomURLId()
            if not self.dbCollection.find_one({'short': id}):
                idUniq = True
                returnedId = id

        return returnedId

    def _uriValidator(self,  url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def _writeLiliURL(self, urlId, urlTarget):
        """ Write in the DB the entry """

        # one record
        entry = {"short": urlId,
                 "urlDst": urlTarget,
                 "date": datetime.datetime.utcnow()
                 }

        entryMongoId = self.dbCollection.insert_one(entry).inserted_id
        if entryMongoId is not None:
            entry["mongoId"] = str(entryMongoId)
        else:
            entry = None

        return entry
