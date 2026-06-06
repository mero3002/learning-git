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

# ------------------------------------------------------------------------------

def updateDB():
    global data
    with open(my_file, 'w') as file:
        json.dump(data, file, indent = 4)

def cleanDB():
    global data, usernames, emails, passwords
    if data:
        data = {}
        usernames = []
        emails = []
        passwords = []
        updateDB()
        return "<< all cleaned >>"
    else:
        return "<< no such database >>"

def readAndValidate():
    username = input("username: ")
    if username in usernames:
        return username
    return False

def createAccount():
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

    usernames.append(username)
    emails.append(email)
    passwords.append(pswd)


    cur_profile = {username : {
        "password" : pswd,
        "email" : email
        }}

    data.update(cur_profile)
    print()
    print("<< Account was added successfully >>")

    updateDB()

def getInfo(username):
    if not data:
        return "<< empty database >>"
    if username in usernames:
        return data.get(username)
    else:
        return "<< Invalid username >>"

def login():
    if not data:
        print("<< empty database >>")
        return
    while True:
        login_username = input("username: ")
        if login_username not in usernames :
            print("<< username does not exist >>")
            continue
        
        login_pswd = input("password: ")
        if login_pswd != getInfo(login_username).get("password"):
            print("<< wrong password >>")
            continue
        print()
        print(f"<< welcome, {login_username} >>")
        break

def deleteAcc(username):
    if username:
        index = usernames.index(username)
        usernames.pop(index)
        emails.pop(index)
        passwords.pop(index)
        del data[username]

        updateDB()
        print("<< user removed successfully >>")
    else:
        print("<< user does not exist >>")

def displayDB():
    if data:
        for key, value in data.items():
            print(f"{key} : {value}")
    else:
        print("<< empty database >>")

def showMenu():
    print("Choose an option:")
    print("1- Login")
    print("2- Create an account")
    print("3- Display database")
    print("4- Get account info")
    print("5- Clear database")
    print("6- Delete an account")
    print("7- Exit")

def startMenu():
    while True:
        showMenu()
        option = input()
        if not option.isdigit():
            print("please enter a numerical value (1-7)")
            print()
            continue

        match int(option):
            case 1:
                print()
                login()
                print()
                continue
            case 2:
                createAccount()
                print()
                continue
            case 3:
                print()
                displayDB()
                print()
                continue
            case 4:
                print()
                if not data:
                    print("<< empty database >>")
                    print()
                    continue

                print(getInfo(readAndValidate()))
                print()
            case 5:
                print("<< Are you sure to delete EVERYTHING? (y/n) >>")
                choice = input()
                if choice == 'y' or choice == 'Y':
                    print()
                    print(cleanDB())
                    print()
                else:
                    print()
                    print("<< task aborted >>")
                    print()
                    continue
            case 6:
                print()
                if not data:
                    print("<< empty database >>")
                    print()
                    continue
                deleteAcc(readAndValidate())
                print()
            case 7:
                print()
                print("<< byebye >>")
                break
            case _:
                print("<< Invalid option >>")
                continue

def main():
    startMenu()

if __name__ == "__main__":
    main()
