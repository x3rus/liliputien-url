#!/usr/bin/python3
#
#####################################

import pymongo
import random
import string
import urllib.parse       # for mongodb password

# self.bd
# self.auth : {'user': "oo" , 'password' : "aaa"}

# connection
# write entry
    # entry not already there
    # validate value before
    # catch BD exception
# search entry
    # manage two resultat choose
    # catch BD exception


class liliputien():
    """backend class, store urls and business logic"""
    def __init__(self, dbLocator='mongodb://%s:%s@localhost:27017/', databaseName="liliputien",
                 collection="dbUrl", user="", passwd=""):
        """Init liliputien"""
        self.dbLocator = dbLocator
        self.user = urllib.parse.quote_plus(user)
        self.passwd = urllib.parse.quote_plus(passwd)
        self.collection = collection
        self.databaseName = databaseName
        self.dbUrls = None

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

    def getRandomURLId(self, size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))
