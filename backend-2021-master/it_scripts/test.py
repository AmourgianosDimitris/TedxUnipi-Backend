import requests
import re

# url = 'http://localhost:8000/api/forms/events/2020/'
# myobj = {
#           "firstname": "Aννα",
#           "lastname": "Noukou",
#           "email": "anna.nooukoou@gmail.com",
#           "phone": 2102513735,
#           "country": "Greece",
#           "street": "Papagou 4",
#           "city": "Attiki",
#           "region": "Nea Filadelfeia",
#           "zip_code": 14342,
#           "notes": ""
#         }
#
# x = requests.post(url, data = myobj)
word = "551552%^&4165)+"
if not re.match("^[0-9+)(]*$", word):
    print ("d")
