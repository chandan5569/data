# Temporary MongoDB insert Whats App group data
import urllib.parse
from time import sleep
import csv
import pymongo
from bson.objectid import ObjectId
import pandas as pd

client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz
collection = db.whatsapp

adminNo = "919773740579"

otherNo = "918097068954 8053007217 917276864773 18059055170"
otherNo = otherNo.split()

groupName = "Testing Group 4"

message = "Welcome"

MemberNo = {'Number': otherNo}
df=pd.DataFrame(data=MemberNo)
MemberNo = df.to_dict("records")

collection.insert_one({"AdminNumber": adminNo, "MemberNumber": MemberNo, "GroupName": groupName, "Message": message})
x = collection.find({})

for y in x:
    print(y['AdminNumber'], y['MemberNumber'], y['GroupName'], y['Message'])