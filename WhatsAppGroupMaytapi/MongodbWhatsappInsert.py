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

otherNo = "18053007217"
otherNo = otherNo.split()

groupName = "Testing WA Group"

message = "Welcome"

MemberNo = {'Number': otherNo}
df=pd.DataFrame(data=MemberNo)
MemberNo = df.to_dict("records")

collection.insert_one({"AdminNumber": adminNo, "MemberNumber": MemberNo, "GroupName": groupName, "Message": message, "Status": "Group not created"})
x = collection.find({"Status": "Group not created"})

for y in x:
    # print(y)
    print(y['AdminNumber'], y['MemberNumber'], y['GroupName'], y['Message'], y['Status'])