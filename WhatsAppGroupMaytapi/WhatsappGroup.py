import requests
import json
import urllib.parse
from time import sleep
import pymongo
from bson.objectid import ObjectId
import pandas as pd


client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz
collection = db.whatsapp
whatsappData = collection.find({})


# Creating the group
for y in whatsappData:
    try:
        numbers = []
        #print(y['AdminNumber'], y['MemberNumber'], y['GroupName'], y['Message'])
        
        #Getting members numbers in list numbers
        for z in y['MemberNumber']:
            numbers.append(z['Number'])

        url1 = 'https://api.maytapi.com/api/d7e6a5cc-3265-4297-9328-4557ba848d39/9977/createGroup'
        headers = {'x-maytapi-key': 'd3c3b5b2-1e42-414f-b53b-0297f67578a1','Content-Type':'application/json','accept':'application/json'}
        
        #adminNo = input("Please enter the group admin's number (country code at front, Ex: 91xxxxxxxxxx):\n")
        adminNo = y['AdminNumber']

        #membersNos = input("Please enter the numbers of group members separated by commas (country code at front, Ex: 91xxxxxxxxxx,91xxxxxxxxxx):\n")

        #groupName = input('Please enter the group name:\n')
        groupName = y['GroupName']

        #phoneNos = membersNos.split(',')
        phoneNos = numbers

        #print(phoneNos)
        dataDict = {'name': groupName, 'numbers': phoneNos}
        #print(dataDict)
        #print(json.dumps(dataDict))
        createGroup = requests.post(url1, headers = headers, data = json.dumps(dataDict))
        createGroupJson = createGroup.json()
        print(createGroupJson)
        groupId = createGroupJson['data']['id']
        #print(groupId)

        url2 = 'https://api.maytapi.com/api/d7e6a5cc-3265-4297-9328-4557ba848d39/9977/sendMessage'
        headers = {'x-maytapi-key': 'd3c3b5b2-1e42-414f-b53b-0297f67578a1','Content-Type':'application/json','accept':'application/json'}

        #message = input('Please enter the message you want to send on the group:\n')
        message = y['Message']

        dataDict = {"to_number": groupId,"type": "text","message": message}
        sendMsg = requests.post(url2, headers = headers, data = json.dumps(dataDict))
        sendMsgJson = sendMsg.json()
        # print(sendMsgJson)

        url3 = 'https://api.maytapi.com/api/d7e6a5cc-3265-4297-9328-4557ba848d39/9977/group/promote'
        headers = {'x-maytapi-key': 'd3c3b5b2-1e42-414f-b53b-0297f67578a1','Content-Type':'application/json','accept':'application/json'}
        adminNo = adminNo + '@c.us'
        data_Dict = {"conversation_id": groupId,"number": adminNo}
        #print(json.dumps(dataDict))
        promoteMember = requests.post(url3, headers = headers, data = json.dumps(data_Dict))
        promoteMemberJson = promoteMember.json()
        #print(promoteMemberJson)
        print("--1 group created--")
    except:
        print("Wrong no in database or Country code in number not found or Mobile is not connected in maytapi")