import requests
import json

# Creating the group
url1 = 'https://api.maytapi.com/api/2ea6dd76-d391-4d2e-a40d-5a5706e40856/9576/createGroup'
headers = {'x-maytapi-key': 'b9ce921c-bd68-4788-93e5-de78525b7647','Content-Type':'application/json','accept':'application/json'}
adminNo = input("Please enter the group admin's number (country code at front, Ex: 91xxxxxxxxxx):\n")
membersNos = input("Please enter the numbers of group members separated by commas (country code at front, Ex: 91xxxxxxxxxx,91xxxxxxxxxx):\n")
groupName = input('Please enter the group name:\n')
phoneNos = membersNos.split(',')
#print(phoneNos)
dataDict = {'name': groupName, 'numbers': phoneNos}
#print(dataDict)
#print(json.dumps(dataDict))
createGroup = requests.post(url1, headers = headers, data = json.dumps(dataDict))
createGroupJson = createGroup.json()
#print(createGroupJson)
groupId = createGroupJson['data']['id']
#print(groupId)

url2 = 'https://api.maytapi.com/api/2ea6dd76-d391-4d2e-a40d-5a5706e40856/9576/sendMessage'
headers = {'x-maytapi-key': 'b9ce921c-bd68-4788-93e5-de78525b7647','Content-Type':'application/json','accept':'application/json'}
message = input('Please enter the message you want to send on the group:\n')
dataDict = {"to_number": groupId,"type": "text","message": message}
sendMsg = requests.post(url2, headers = headers, data = json.dumps(dataDict))
sendMsgJson = sendMsg.json()
#print(sendMsgJson)

url3 = 'https://api.maytapi.com/api/2ea6dd76-d391-4d2e-a40d-5a5706e40856/9576/group/promote'
headers = {'x-maytapi-key': 'b9ce921c-bd68-4788-93e5-de78525b7647','Content-Type':'application/json','accept':'application/json'}
adminNo = adminNo + '@c.us'
data_Dict = {"conversation_id": groupId,"number": adminNo}
#print(json.dumps(dataDict))
promoteMember = requests.post(url3, headers = headers, data = json.dumps(data_Dict))
promoteMemberJson = promoteMember.json()
#print(promoteMemberJson)


