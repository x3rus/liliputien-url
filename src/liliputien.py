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

# self.bd
# self.auth : {'user': "oo" , 'password' : "aaa"}

# connection
# write entry
#    # entry not already there
#    # validate value before
#    # catch BD exception
# search entry
#    # manage two resultat choose
#    # catch BD exception


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

        if mongoSrv.is_mongos:
            # Select DB  / create it
            liliDb = mongoSrv[self.databaseName]
            self.dbCollection = liliDb.dbUrl                 # TODO check to use self.collection intend of dbUrl
            return self.dbCollection

        return None

    def getRandomURLId(self, size=None, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        """ Generate the random ID /fk8dS3 """
        if size is None:
            size = self.idSize
        return ''.join(random.choice(chars) for _ in range(size))

    def getUniqUrlId(self, size=None, maxRetry=3):
        """ Return Url ID uniq validat with the DB """
        if size is None:
            size = self.idSize

        idUniq = False
        returnedId = None
        count = 0
        # check if it's already in the DB
        while idUniq is False and count <= maxRetry:
            count += 1
            id = self.getRandomURLId()
            if not self.dbCollection.find_one({'short': id}):
                idUniq = True
                returnedId = id

        return returnedId

    def uriValidator(self,  url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def addUrlRedirection(self, urlDestination):
        """add an entry in mongodb, validate the entry
            return : dictionnary with url info
            raise : liliputienErrors.urlDontMatchCriteria
        """

        if not self.uriValidator(urlDestination):
            raise liliputienErrors.urlDontMatchCriteria

        urlId = self.getUniqUrlId()
        if urlId is None:
            raise liliputienErrors.unableGettingUniqUrlID

        MongoEntry = self.writeLiliURL(urlId, urlDestination)
        if MongoEntry is None:
            raise liliputienErrors.unableWritingUrlEntry

        return MongoEntry

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

    # def test_getUniqIdFalse(self):
        # need learn mock mongodb + decorate method generateRandomId

    def writeLiliURL(self, urlId, urlTarget):
        """ Write in the DB the entry """

        # one record
        entry = {"short": "/" + urlId,
                 "urlDst": urlTarget,
                 "date": datetime.datetime.utcnow()
                 }

        entryMongoId = self.dbCollection.insert_one(entry).inserted_id
        if entryMongoId is not None:
            entry["mongoId"] = str(entryMongoId)
        else:
            entry = None

        return entry
