import os
import json
print("---------- Login Manager ----------")

my_file = "file.json"
data = {}
if os.path.exists(my_file):
    with open(my_file, "r") as file:
        data = json.load(file)

usernames = []
emails = []
passwords = []

for key in data.keys():
    usernames.append(key)

for value in data.values():
    emails.append(value.get("email"))
    passwords.append(value.get("password"))

#for i in range(len(emails)):
#    print(usernames[i])
#    print(emails[i])
#    print(passwords[i])
#    print()

while True:
    username = input("username: ")

    if username in usernames:
        print("username isn't valid")
        continue

    else:
        break

while True:
    email = input("email: ")
    
    if email in emails:
        print("email isn't valid")
        continue

    else:
        break

pswd = input("password: ")

cur_profile = {username : {
    "password" : pswd,
    "email" : email
    }}

data.update(cur_profile)

with open(my_file, "w") as file:
    json.dump(data, file, indent = 4)

#if os.path.exists(my_file):
#    os.remove(my_file)
#    print("JSON file was deleted")
