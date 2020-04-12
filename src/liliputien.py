#!/usr/bin/python3
#
#####################################

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
        self.dbUrls = None
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
            self.dbUrls = liliDb.dbUrl                 # TODO check to use self.collection intend of dbUrl
            return self.dbUrls

        return None

    def getRandomURLId(self, size=None, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        """ Generate the random ID /fk8dS3 """
        if size is None:
            size = self.idSize
        return ''.join(random.choice(chars) for _ in range(size))

    def uriValidator(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def addUrlRedirection(self, urlDestination):
        """add an entry in mongodb, validate the entry
            return : urlID
        """

        # TODO Q: est-ce que je devrais avoir des exceptions thrower
        if not self.uriValidator(urlDestination):
            raise liliputienErrors.urlDontMatchCriteria

        # get unid and confirme it
        # write it 
        # return the ID 
        urlID = None
        urlID = self.getRandomURLId()
        return urlID
