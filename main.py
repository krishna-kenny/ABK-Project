#

import pickle as p
import mysql.connector as ms

conn = ms.connect(
    host="localhost",
    user="root",
    password="dpsbn"
)

cur = conn.cursor(buffered = True)

cur.execute("create database if not exists gym;")
cur.execute("use gym;")

cur.execute("""
CREATE TABLE if not exists user(
    uid int PRIMARY KEY auto_increment,
    name varchar(50), 
    account_lvl varchar(2),
    pid int, 
    cost int,
    phone int(10),
    address VARCHAR(200),
    password varchar(25)  
);
""")

cur.execute("""
CREATE TABLE if not exists plans(
    pid int primary key,
    pname varchar(50),
    pduration varchar(25) not null,
    pcost int not null 
);
""")

cur.execute("""
CREATE TABLE if not exists bill(
    bid int primary key not null auto_increment,
    bdate date not null,
    buid int,
    bname varchar(50), 
    bcost int not null
);
""")

cur.execute("""insert into plans values(
    (1, )

);""")

cur.execute("insert into user values(null, 'krishna', 'II', 4, 12500, '1234567890', 'address', '!@#$');")

def encrypt(p):
    key = {"0": ")","1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "("}
    password = ""
    for l in p:
        password += key[l]
    return password



def decrypt(p):
    inv_key = {v: k for k, v in {"0": ")","1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "("}.items()}
    password = ""
    for l in p:
        password += inv_key[l]
    return password



#common to user and admin
def new_account():
    name = input("name: ")
    password = input("password [number only]: ")
    print("""
    plans:
        1] day    | 200
        2] week   | 500
        3] month  | 1500
        4] year   | 12500      
""")
    plan = input("plan [enter number]: ")
    cur.execute(f"select pcost from plans where pid = '{plan}'")
    cost = cur.fetchone()[0]
    ph = input("phone: ")
    addr = input("address: ") 
    cur.execute(f"insert into user values(NULL, '{name}', 'I', {plan}, {cost}, '{ph}', '{addr}', '{encrypt(password)}');")
    print("your account has been created.")



def del_account(uid):

    if input("are you sure? [yes/no]: ") == "no":
        return 0
    else:

        if cur.execute(f"select account_lvl from user where uid = {uid};") == "I":
            cur.execute(f"delete from user where uid = {uid};")            
        else:
            acc = input("uid account to be deleted: ")
            cur.execute(f"delete from user where uid = {acc};")

        print("the account is now deleted.")

    cur.fetchall()



def change_plan(uid):

    print("""
    plans:
        1] day    | 200
        2] week   | 500
        3] month  | 1500
        4] year   | 12500      
""")    

    if cur.execute(f"select account_lvl from user where uid = {uid};") == "I":
        plan = input("new plan [enter number]: ")
        cur.execute(f"update user pid = {plan} where uid = {uid};")            
    else:
        acc = input("uid account to be changed: ")
        plan = input("new plan [enter number]: ")
        cur.execute(f"update user pid = {plan} where uid = {acc};")
            
    print("the account is now deleted.")

    cur.fetchall()


#user only
def bill(uid):

    if input("are you sure [yes/no]: ") == "no":
        return 0
    else:

        user_rec = cur.execute(f"select * from user where uid = {uid};")
        print(f"""
    bill preview:   [ bid | current_date() | {user_rec[0]} | {user_rec[1]} | {user_rec[4]} ]      
""")
        if input("proceed? [yes/no]: ") == "no":
            return 0
        else:
            cur.execute(f"insert into bill values(null, current_date(), {user_rec[0]}, {user_rec[1]}, {user_rec[4]});")
            print("you have been billed successfully.")

    cur.fetchall()
          
        
#admin only
def display_all(uid):
    inp = input("""
    tables: 
        1] user
        2] plans
        3] bill
""")
    dct = {
        "1": "user",
        "2": "plans",
        "3": "bill"
    }
    for rec in cur.execute(f"select * from {dct[inp]};"):
        print(rec)

    cur.fetchall()



def god_mode(uid):
    if cur.execute(f"select account_lvl from user where uid = {uid};") == "I":
        return 0
    else:
        command = input("enter mysql update command:\n")
        cur.execute(f"{command}")
        print("data updated.")

    print(cur.fetchall())



#log in
def log_in(uid):
    cur.execute(f"select name from user where uid = {uid};")
    print(f"Welcome back {cur.fetchone()[0]}")
    cur.execute(f"select account_lvl from user where uid = {uid};")

    if cur.fetchone()[0] == "I":
        
        while True:
            b = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|                                                                |
|    1] see your gym information                                 |
|                                                                |
|    2] change plan                                              |
|                                                                |
|    3] logout

     4]delete account                                            |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
""")
            if b == "1":
                cur.execute(f"select * from user where uid = {uid};")
                print(cur.fetchone())
            elif b == "2": 
                change_plan(uid)
            elif b == "3":
                break
            elif b == "4":
                del_account(uid)
            else:
                print("invalid input")
        
    else:

        while True:
            b = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|                                                                |
|    1] see your gym information

    2] change your plan.

     3]see all gym members's information                                 |
|                                                                |
|    4] update any record  

    5]delete any record                                      |
|                                                                |
|    6] logout                                                   |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
""")
            if b == "1":
                cur.execute(f"select * from user where uid = {uid};")
                print(cur.fetchone())
            elif b == "2": 
                change_plan(uid)
            elif b == "3":
                cur.execute(f"select * from user;")
                for line in cur.fetchall():
                    print(line)
            elif b == "4":
                god_mode(uid)
            elif b == "5":
                del_account(uid)
            elif b == "6":
                break
            else:
                print("invalid input")
    cur.fetchall()
    


while True:
    inp = input("""
    MENU:   
        1] log in
        2] new account
        3] exit    
""")

    if inp == "1":
        username = input("username: ")
        password = input("password: ")
        cur.execute(f"select count(uid) from user where name = '{username}' and password = '{encrypt(password)}';")

        if cur.fetchone() == "0":
            print("incorrect details.")
            continue
        else:
            cur.execute(f"select uid from user where name = '{username}' and password = '{encrypt(password)}';")
            uid = cur.fetchone()[0]
            print(uid)
            log_in(uid)
                   

    elif inp == "2":
        new_account()

    elif inp == "3":
        break

    else:
        print("invalid input")

print("thank you")

cur.close()
conn.close()