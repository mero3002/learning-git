import os
import json
import random
print("=================================")
print("          Login Manager")
print("=================================")
print()

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

# print("Token:")
# print(token)
# print()

# ----------------------------------------------------------------------------------------------------------
# preparing data:

data = {} # the only source of truth now

with open(data_file, 'r') as file:
    data = json.load(file)

mode = "guest"
logged_in_username = ""

halt = False

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
        if does_user_exist(username):
            print("<< username is taken >>")
            print()
            continue
        return username

def read_new_email():
    while True:
        email = read_email()
        if does_email_exist(email):
            print("<< email is already registered >>")
            print()
            continue
        return email

def read_token():
    token_in = input("admin token: ")
    return token_in

def read_new_token():
    global token
    print(f"Old token: {token}")
    while True:
        new_token = input("New token: ")
        if new_token == token:
            print("<< you can't use an old token >>")
            print()
            continue
        if len(new_token) != 4:
            print("<< token's length must be equal to 4 >>")
            print()
            continue
        break
    return new_token
    
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
        print("<< all wiped >>")
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

def make_me_admin():
    global mode

    if is_token(read_token()):
        mode = "admin"
        print("<< you've become an admin >>")
        return
    
    print("<< wrong token, task aborted >>")

def make_me_user(username):
    global mode, logged_in_username
    logged_in_username = username
    mode = "user"

# ----------------------------------------------------------------------------------------------------------
# getters:

def get_password(username):
    return (data.get(username)).get("password")

def get_email(username):
    return (data.get(username)).get("email")

# ----------------------------------------------------------------------------------------------------------

def change_token():
    if mode != "admin":
        print("<< Unauthorized >>")
        return
    
    new_token = read_new_token()
    with open(token_file, 'w') as file:
        file.write(new_token)
    print("<< token updated successfully >>")
    update_token()

def verify_delete_account(username):
    if mode == "admin":
        option = input("Are you sure to delete this account? (y/n) ").lower()
        if option == "y":
            delete_account(username)
        else:
            print("<< Task aborted >>")

    elif mode == "user":
        option = input("Are you sure to delete your account? (y/n) ").lower()
        if option == "y":
            if read_password() != get_password(username):
                print("<< wrong password, Task aborted >>")
                return
            delete_account(username)
        else:
            print("<< Task aborted >>")

def verify_clear_db():
    if mode != "admin":
        print("<< Unauthorized >>")
    elif not data:
        print("<< no such database >>")
    else:
        option = input("Are you sure to delete the database? (y/n) ").lower()
        if option == "y":
            clean_db()
        else:
            print("<< Task aborted >>")

def verify_update_info(username):
    if read_password() != get_password(username):
        print("<< wrong password, Task aborted >>")
        # print()
        return False
    else:
        # print()
        update_info(username)

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
        password = read_password()
        if password != get_password(username):
            trials -= 1

            if not trials:
                print()
                print("<< Too many failed attempts, task aborted >>")
                return False
            
            print()
            print(f"<< wrong password, {trials} trial/s left >>")
            continue
        else:
            return username

# def action_verification(action, username=None):
    # match action:
    #     case "delete my account":
    #         option = input("Are you sure to delete your account? (y/n) ")
    #         if option.lower == 'y':
    #             delete_account(username)
    #         else:
    #             print("<< Task aborted >>")

    #     case "delete an account":
    #         option = input("Are you sure to delete this account? (y/n) ")
    #         if option.lower == 'y':
    #             delete_account(username)
    #         else:
    #             print("<< Task aborted >>")
            
    #     case "clear the database":
    #         option = input("Are you sure to delete the database? (y/n) ")
    #         if option.lower == 'y':
    #             clean_db()
    #         else:
    #             print("<< Task aborted >>")

def create_account():
    username = read_new_username()
    email = read_new_email()
    pswd = read_password()

    cur_profile = {username : {
        "password" : pswd,
        "email" : email
        }}

    if mode == "guest":
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
    global mode, logged_in_username
    logged_in_username = None
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
    print()
    old_email = (data.get(username)).get("email")
    print(f"Old email: {old_email}")
    print("NEW", end=" ")
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
    global halt
    halt = True
    print("<< byebye >>")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# show menus:

def show_guest_menu():
    print(":: GUEST ::")
    print("[1] Login")
    print("[2] Create an account")
    print("[3] Enter admin mode")
    print("[4] Exit app")

def show_user_menu():
    print(f":: USER | {logged_in_username} ::")
    print("[1] Display my info")
    print("[2] Update my info")
    print("[3] Delete my account") # verification
    print("[4] Exit app")
    print("[5] Log out")

def show_admin_menu():
    print(":: ADMIN ::")
    print("[1] Display database")
    print("[2] Add an account")
    print("[3] View account")
    print("[4] Update an account's info")
    print("[5] Delete an account")
    print("[6] Clear database") #verification
    print("[7] Change token key")
    print("[8] Exit app")
    print("[9] Log out")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# start menus:

def general_start():
    global mode
    while not halt:
        match mode:
            case "guest":
                guest_start_menu()
            case "user":
                user_start_menu()
            case "admin":
                admin_start_menu()

def guest_start_menu():
    show_guest_menu()
    option = check_option(4)
    if not option:
        return

    print()
    match int(option):
        case 1:
            login()
        case 2:
            create_account()
        case 3:
            make_me_admin()
        case 4:
            byebye()
        case _:
            print("<< Invalid option, enter (1-4) >>")
    print()

def user_start_menu():
    show_user_menu()
    option = check_option(5)
    if not option:
        return

    print()
    match int(option):
        case 1:
            get_info(logged_in_username)
        case 2:
            verify_update_info(logged_in_username)
        case 3:
            verify_delete_account(logged_in_username)
        case 4:
            byebye()
        case 5:
            logout()
            print("<< logged out >>")
        case _:
            print("<< Invalid option, enter (1-5) >>")
    print()

def admin_start_menu():
    show_admin_menu()
    option = check_option(9)
    if not option: 
        return 

    print()
    match int(option):
        case 1:
            display_db()
        case 2:
            create_account()
        case 3:
            if not data:
                print("<< empty database >>")
            else:
                get_info(read_username())
        case 4:
            if not data:
                print("<< empty database >>")
            else:
                update_info(read_username())
        case 5:
            if not data:
                print("<< empty database >>")
            else:
                verify_delete_account(read_username())
        case 6:
            verify_clear_db()
        case 7:
            change_token()
        case 8:
            byebye()
        case 9:
            logout()
            print("<< logged out >>")
        case _:
            print("<< Invalid option, enter (1-9) >>")
    print()

def check_option(n):
    option = input()
    if not option.isdigit():
        print(f"please enter a numerical value (1-{n})")
        print()
        return False
    return option

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    general_start()

if __name__ == "__main__":
    main()