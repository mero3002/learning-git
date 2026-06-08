import os
import json
import random
print("---------- Login Manager ----------")

# healing the json
data_file = "file.json"

def create_json():
    with open(data_file, 'w') as file:
        json.dump({}, file, indent = 4)

if not os.path.exists(data_file):                                 # doesn't exist
    create_json()
    
else:    
    try:
        with open(data_file, 'r') as file:
            contents = json.load(file) # i don't really need the 'contents' dict, it's just there to test json.load
    except ValueError:                                          # exists corrupted
        create_json()

# ----------------------------------------------------------------------------------------------------------
# healing the token file:

token_file = "admin_token.txt"
token = ""

def create_token_file():
    chars_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:'\",<>/?|`~"

    with open(token_file, 'a') as file:
        for i in range(4):
            file.write(random.choice(chars_str))

def update_token():
    global token
    with open(token_file, 'r') as file:
        token = file.read()

if os.path.exists(token_file):
    with open(token_file, 'r') as file:
        content = file.read().strip()
        # content = file.read() # 5555555555555

    if len(content) != 4:
        # print(f"content : {repr(content)}")
        # print(f"which is : {len(content)} char/s")
        os.remove(token_file)
        create_token_file()
else:
    create_token_file()

update_token()

print("Token:")
print(token)
print()

# ----------------------------------------------------------------------------------------------------------
# preparing data:

data = {} # the only source of truth now

with open(data_file, 'r') as file:
    data = json.load(file)

mode = "guest"
logged_in_username = ""

hault = False

# ----------------------------------------------------------------------------------------------------------
# readers:

def read_username():
    username = input("username: ")
    return username

def read_email():
    email = input("email: ")
    return email

def read_password():
    pswd = input("password: ")
    return pswd

def read_new_username():
    while True:
        username = read_username()
        if does_email_exist(username):
            print("<< username is taken >>")
            continue
        return username

def read_new_email():
    while True:
        email = read_email()
        if does_email_exist(email):
            print("<< email is already registered >>")
            continue
        return email

def read_token():
    token_in = input("admin token: ")
    return token_in

# ----------------------------------------------------------------------------------------------------------
# DB:

def update_db():
    global data
    with open(data_file, 'w') as file:
        json.dump(data, file, indent = 4)

def clean_db():
    global data
    if data:
        data = {}
        update_db()
        print("<< all cleaned >>")
    else:
        print("<< no such database >>")

def display_db():
    if data:
        for key, value in data.items():
            print(f"{key} : {value}")
    else:
        print("<< empty database >>")

# ----------------------------------------------------------------------------------------------------------
# does exist?

def does_email_exist(email):
    for value in data.values():
        if value.get("email") == email:
            return True
    return False

def does_user_exist(username):
    if username in data:
        return True
    return False

# ----------------------------------------------------------------------------------------------------------
# Make me:

    token_in = input("admin token: ")
    if token_in == token:
        return True
    return False

def make_me_admin():
    global mode

    if is_token(read_token()):
        mode = "admin"
        print("<< you've became an admin >>")
        return
    
    print("<< wrong token, task aborted >>")

def make_me_user(username):
    global mode, logged_in_username
    logged_in_username = username
    mode = "user"

# ----------------------------------------------------------------------------------------------------------

def authenticate_user():
    while True:
        username = read_username()
        if not does_user_exist(username):
            print("<< username does not exist >>")
            continue
        else:
            break

    trials = 3
    while True:
        if trials == 0:
           print("<< Authentication failed, task aborted >>")
           return False 
        
        password = read_password()
        if password != get_password(username):
            trials -= 1
            print(f"<< wrong password, {trials} trial/s left >>")
            continue
        else:
            return username

def get_password(username):
    return (data.get(username)).get("password")

def get_email(username):
    return (data.get(username)).get("email")

def create_account():
    username = read_new_username()
    email = read_new_email()
    pswd = read_password()

    cur_profile = {username : {
        "password" : pswd,
        "email" : email
        }}

    make_me_user(username)
    data.update(cur_profile)
    print()
    print("<< account was added successfully >>")

    update_db()

def get_info(username):
    if not data:
        print("<< empty database >>")
        return

    if does_user_exist(username):
        print(data.get(username))
        return

    print("<< invalid username >>")

def login():
    if not data:
        print("<< empty database >>")
        return
    
    login_username = authenticate_user()
    if login_username:
        make_me_user(login_username)
        print()
        print(f"<< welcome, {login_username} >>")

def logout():
    global mode
    # print("<< logged out >>")
    mode = "guest"

def delete_account(username):
    if does_user_exist(username):
        del data[username]
        update_db()
        print("<< user removed successfully >>")

        if mode == "user":
            logout()
    else:
        print("<< user does not exist >>")

def update_info(username):
        
    if not does_user_exist(username):
        print("<< username does not exist >>")
        return

    old_email = (data.get(username)).get("email")
    print(f"account's old email: {old_email}")
    print("enter a new one below")
    new_email = read_new_email()

    old_pswd = (data.get(username)).get("password")
    while True:
        new_pswd = input(f"NEW password: ")
        if new_pswd == old_pswd:
            print("<< you cannot use an old password >>")
            continue

        data.update({username : {"password" : new_pswd,
                                 "email" : new_email
                                 }})
        update_db()
        print()
        print("<< info updated successfully >>")
        break

def is_token(token_in):
    return token_in == token

def byebye():
    global hault
    hault = True
    print("<< byebye >>")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# show menus:

def show_guest_menu():
    print("<< guest >>")
    print("1- Login")
    print("2- Create an account")
    print("3- Enter admin mode")
    print("4- Exit app")

def show_user_menu():
    print(f"<< user: {logged_in_username} >>")
    print("1- Display my info")
    print("2- Update my info")
    print("3- Delete my account") # verification
    print("4- Get my account info")
    print("5- Exit app")
    print("6- Log out")

def show_admin_menu():
    print("<< admin >>")
    print("1- Display database")
    print("2- Get an account's info")
    print("3- Update an account's info")
    print("4- Delete an account")
    print("5- Clear database") #verification
    print("6- Exit app")
    print("7- Log out")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# start menus:

def general_start():
    global mode
    while not hault:
        match mode:
            case "guest":
                guest_start_menu()
            case "user":
                user_start_menu()
            case "admin":
                admin_start_menu()

def guest_start_menu():
    show_guest_menu()
    option = input()
    if not option.isdigit():
        print("please enter a numerical value (1-4)")
        print()

    match int(option):
        case 1:
            print()
            login()
            print()
        case 2:
            print()
            create_account()
            print()
        case 3:
            print()
            make_me_admin()
            print()
        case 4:
            print()
            byebye()
            print()
        case _:
            print("\n<< Invalid option, enter (1-4) >>\n")

def user_start_menu():
    show_user_menu()
    option = input()
    if not option.isdigit():
        print("please enter a numerical value (1-6)")
        print()
        return

    match int(option):
        case 1:
            print()
            get_info(logged_in_username)
            print()
        case 2:
            print()
            update_info(logged_in_username)
            print()
        case 3:
            print()
            delete_account(logged_in_username)
            print()
        case 4:
            print()
            get_info(logged_in_username)
            print()
        case 5:
            print()
            byebye()
            print()
        case 6:
            print()
            logout()
            print("<< logged out >>")
            print()
        case _:
            print("\n<< Invalid option, enter (1-6) >>\n")

def admin_start_menu():
    show_admin_menu()
    option = input()
    if not option.isdigit():
        print("please enter a numerical value (1-8)")
        print()
        return

    match int(option):
        case 1:
            print()
            display_db()
            print()
        case 2:
            print()
            get_info(read_username())
            print()
        case 3:
            print()
            update_info(read_username())
            print()
        case 4:
            print()
            delete_account(read_username())
            print()
        case 5:
            print()
            clean_db()
            print()
        case 6:
            print()
            byebye()
            print()
        case 7:
            print()
            logout()
            print("<< logged out >>")
            print()
        case _:
            print("\n<< Invalid option, enter (1-6) >>\n")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    general_start()

if __name__ == "__main__":
    main()