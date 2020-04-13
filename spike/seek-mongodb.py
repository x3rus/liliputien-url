#!/usr/bin/python3
#
###########################################################

import pymongo
import pprint
import datetime
import urllib.parse       # for mongodb password

# Connect
username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('ze_password')
mongoSrv = pymongo.MongoClient('mongodb://%s:%s@localhost:27017/' % (username, password))

# Select DB  / create it
liliDb = mongoSrv["liliputien"]

# one record
post = {"short": "/Dk8c3",
        "url": "http://www.google.com",
        "date": datetime.datetime.utcnow()
        }

dbUrl = liliDb.dbUrl
post_id = dbUrl.insert_one(post).inserted_id
print(post_id)


# loop record
for post in dbUrl.find():
    pprint.pprint(post)

# search on record
print(10 * "=")

my_posts = dbUrl.find({"short": "/Dk8c3"})
pprint.pprint(my_posts[0])

print(10 * "=")
print(dbUrl.count_documents({"short": "/Dk8c3"}))

dbUrl.delete_many({"short": "/Dk8c3"})
