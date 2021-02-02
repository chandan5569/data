import pymongo
import urllib.parse
import dns
from mongoengine import *
import sys

user_name = sys.argv[1]
otp = (sys.argv[2])
# print(user_name)
# print(otp)
client = pymongo.MongoClient('mongodb+srv://bilalm:' + urllib.parse.quote_plus('Codemarket.123') + '@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
my_db = client['dreamjobpal']
otp_db = my_db.linkedin_otp

result = otp_db.update_many( 
        {"linkedin_login_url":user_name, "Status":"OTP sent"}, 
        { "$set":{ "Status":"OTP updated","OTP":otp }},
         
                        )

