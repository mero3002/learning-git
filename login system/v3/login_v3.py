import os
import json
print("---------- Login Manager ----------")

# Healing the JSON
my_file = "file.json"

#with open(my_file, 'r') as file:
#    content = json.load(file)

def createJson():
    with open(my_file, 'w') as file:
        json.dump({}, file, indent = 4)

if not os.path.exists(my_file):                                 # doesn't exist
    createJson()
    
else:    
    try:
        with open(my_file, 'r') as file:
            contents = json.load(file)
    except ValueError:                                          # exists corrupted
        createJson()
# ------------------------------------------------------------------
        
data = {} # the only source of truth now

with open(my_file, 'r') as file:
    data = json.load(file)
        
# ------------------------------------------------------------------
def updateDB():
    global data
    with open(my_file, 'w') as file:
        json.dump(data, file, indent = 4)

def cleanDB():
    global data
    if data:
        data = {}
        updateDB()
        return "<< all cleaned >>"
    else:
        return "<< no such database >>"

def readUsername():
    username = input("username: ")
    return username

def readEmail():
    email = input("email: ")
    return email

def doesEmailExist(email):
    for value in data.values():
        if value.get("email") == email:
            return True
    return False

def doesUserExist(username):
    if username in data:
        return True
    return False

def createAccount():
    while True:
        username = readUsername()
        if doesUserExist(username):
            print("username isn't valid")
            continue

        else:
            break

    while True:
        email = readEmail()
        if doesEmailExist(email):
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
    print()
    print("<< account was added successfully >>")

    updateDB()

def getInfo(username):
    if not data:
        return "<< empty database >>"

    if doesUserExist(username):
        return data.get(username)

    return "<< invalid username >>"

def login():
    if not data:
        print("<< empty database >>")
        return
    while True:
        login_username = readUsername()
        if not doesUserExist(login_username):
            print("<< username does not exist >>")
            continue
        break
    expectedPswd = getInfo(login_username).get("password")

    while True:
        login_pswd = input("password: ")
        if login_pswd != expectedPswd:
            print("<< wrong password >>")
            continue
        break

    print()
    print(f"<< welcome, {login_username} >>")

def deleteAcc(username):
    if doesUserExist(username):
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

def updateInfo():
    while True:
        username = readUsername()
        if not doesUserExist(username):
            print("<< username does not exist >>")
            continue
        break

    old_email = (data.get(username)).get("email")
    while True:
        print(f"your old email is: {old_email}")
        new_email = input("NEW email: ")
        if new_email == old_email:
            print("<< you cannot use an old email >>")
            continue
        elif doesEmailExist(new_email):
            print("<< email already exists, try another >>")
            continue
        break

    old_pswd = (data.get(username)).get("password")
    while True:
        new_pswd = input(f"NEW password: ")
        if new_pswd == old_pswd:
            print("<< you cannot use an old password >>")
            continue

        data.update({username : {"password" : new_pswd,
                                 "email" : new_email
                                 }})
        updateDB()
        print()
        print("<< info updated successfully >>")
        break

def showMenu():
    print("Choose an option:")
    print("1- Login")
    print("2- Create an account")
    print("3- Display database")
    print("4- Get account info")
    print("5- Clear database")
    print("6- Delete an account")
    print("7- Update account info")
    print("8- Exit")

def startMenu():
    while True:
        showMenu()
        option = input()
        if not option.isdigit():
            print("please enter a numerical value (1-8)")
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

                print(getInfo(readUsername()))
                print()
            case 5:
                if not data:
                    print("\n<< empty database >>\n")
                    continue

                print("<< are you sure to delete EVERYTHING? (y/n) >>")
                choice = input()
                if choice == 'y' or choice == 'Y':
                    print()
                    print(cleanDB())
                    print()
                else:
                    print("\n<< task aborted >>\n")
                    continue
            case 6:
                print()
                if not data:
                    print("<< empty database >>\n")
                    continue
                deleteAcc(readUsername())
                print()
            case 7:
                updateInfo()
                print()
            case 8:
                print("\n<< byebye >>\n")
                break
            case _:
                print("\n<< Invalid option >>\n")
                continue

def main():
    startMenu()

if __name__ == "__main__":
    main()