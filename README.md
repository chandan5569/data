# data

Hi!
I have recently added whatsappgroup.py. 

Please change the username and path in the config.py file based on your platform.
It will ensure that you do not have to scan the QR more than twice. 
If it shows the user data direction is not unique error, you need to go to the directory where user data
is situated and delete the Wtsp folder. 
Please refer to the config.py file for more details. 

If script.py quits unexpectedly, check your internet connectivity. 
As the task is to automate the browser, the program is susceptible to network fluctuations. Please try again. 
Additionally, you can increase the time in the implicitly_wait() function under the setUp function of whatsappgroup.py 
(15-20 would be the recommended maximum). 

Feel free to report any issues and queries. 
