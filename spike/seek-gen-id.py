#!/usr/bin/python3
#
####################################################

# ref : https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

randomListRnd= {}
countRnd = 0
for x in range(1,5):
    zeIdRnd = id_generator()
    if zeIdRnd in randomListRnd.keys():
        # print("ERROR, key already there for Rnd")
        countRnd += 1
    else:
        randomListRnd[id_generator]="ok"

print(10 * "=")
##################################################

# ref : https://stackoverflow.com/a/17323913
import uuid

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

randomListUUID= {}
countUUID = 0 
for x in range(1,100000):
    zeId = my_random_string(6)
    if zeId in randomListUUID.keys():
        # print("ERROR, key already there for UUID")
        countUUID += 1
    else:
        randomListUUID[zeId]="ok"

print("total count UUID with conflit : ", countUUID)
print("total count RND with conflit : ", countRnd)
# Note : my problem with this one is no uppercase , so less 
