import pymongo
import urllib.parse
import dns
from mongoengine import *
import sys

user_name = sys.argv[1]
otp = sys.argv[2]

client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz #db
otp_collection = db.OTP_linkedin #collection

findUser = otp_collection.find({"linkedin_login_url":user_name, "Status":"OTP sent"})
if list(findUser):
    result = otp_collection.update_one( 
        {"linkedin_login_url":user_name, "Status":"OTP sent"}, 
        { "$set":{ "Status":"OTP updated","OTP":otp }},
        )
    print("Otp Updated...")
else:
    print("User Name not found...")