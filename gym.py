import mysql.connector as ms
from datetime import datetime
from tabulate import tabulate

conn = ms.connect(
        host = "localhost",
        user = "root",
        password = "dpsbn",
        autocommit = True
)

cur = conn.cursor()

cur.execute("create database if not exists gym;")
cur.execute("use gym;")

cur.execute("""
CREATE TABLE if not exists user(
    uid int PRIMARY KEY auto_increment,
    name varchar(50),
    account_lvl varchar(2),
    pid int,
    cost int,
    phone varchar(15),
    address VARCHAR(200),
    password varchar(25)
);
        """)

cur.execute("""
CREATE TABLE if not exists plans(
    pid int primary key,
    pname varchar(50),
    pduration int,
    pcost int not null
);
        """)

cur.execute("""
CREATE TABLE if not exists bill(
    bid int primary key auto_increment,
    bdate date not null,
    buid int,
    bname varchar(50),
    bcost int not null
);
        """)


cur.execute("select count(uid) from user;")
if cur.fetchone()[0] == 0:
cur.execute("""insert into plans values
    (1, "day", 1, 200),
    (2, "week", 7, 500),
    (3, "month", 30, 1500),
    (4, "year", 365, 12500)
    ;""")
cur.execute("insert into user values (1, 'k', 'II', 4, 12500, '1234567890', 'address', '!@#$');")



def encrypt(p):
key = {
        "0": ")","1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "("
}
password = ""
for l in p:
password += key[l]
return password



def decrypt(p):
inv_key = {
        v: k for k, v in {
                "0": ")","1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "("
        }.items()}
password = ""
for l in p:
password += inv_key[l]
return password



#common to user and admin
def new_account():

try:
name = input("name: ")
password = input("password [number only]: ")
print("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|    plans:                                                      |
|----------------------------------------------------------------|
|        1] day    | 200                                         |
|        2] week   | 500                                         |
|        3] month  | 1500                                        |
|        4] year   | 12500                                       |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
        """)
plan = input("plan [enter number]: ")
cur.execute(f"select pcost from plans where pid = ' {
        plan
}'")
cost = cur.fetchone()[0]
ph = input("phone: ")
addr = input("address: ")
cur.execute(f"insert into user values(NULL, ' {
        name
}', 'I', {
        plan
}, {
        cost
}, ' {
        ph
}', ' {
        addr
}', ' {
        encrypt(password)}');")
print("your account has been created.")

except:
print("error")



def del_account(uid):

try:
if input("are you sure? [yes/no]: ") == "yes":
cur.execute(f"select account_lvl from user where uid = {
        uid
};")
if cur.fetchone()[0] == "I":
cur.execute(f"delete from user where uid = {
        uid
};")
else :
acc = input("uid of account to be deleted: ")
cur.execute(f"delete from user where uid = {
        acc
};")

print("the account is now deleted.")
return 0

else :
return 0


except:
print("error")



def change_plan(uid):
plans = {
        1:"200", 2:"500", 3:"1500", 4:"15000"
}
try:
print("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|    plans:                                                      |
|----------------------------------------------------------------|
|        1] day    | 200                                         |
|        2] week   | 500                                         |
|        3] month  | 1500                                        |
|        4] year   | 12500                                       |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
    """)
cur.execute(f"select account_lvl from user where uid = {
        uid
};")
if cur.fetchone()[0] == "I":
plan = int(input("new plan [enter number]: "))
p = plans[plan]
cur.execute(f"update user set pid = {
        plan
}, cost = {
        p
} where uid = {
        uid
};")
else :
uid = int(input("uid of account to be changed: "))
plan = int(input("new plan [enter number]: "))
p = plans[plan]
cur.execute(f"update user set pid = {
        plan
}, cost = {
        p
} where uid = {
        uid
};")

print("the account plan is now updated.")

except:
print("error")


#user only
def bill(uid):
try:


if input("are you sure [yes/no]: ") == "yes":

cur.execute(f"select * from user where uid = {
        uid
};")
user_rec = cur.fetchone()
head = ["bill ID", "date", "user ID", "username", "amount"]
bill_row = ["bid", f" {
        datetime.date(datetime.now())}", f" {
        user_rec[0]}", f" {
        user_rec[1]}", f" {
        user_rec[4]}"]

print(f"""
        bill preview:
    """)
print(tabulate([head, bill_row]))

if input("proceed? [yes/no]: ") == "yes":
date = datetime.date(datetime.now())
cur.execute(f"insert into bill values (NULL, ' {
        date
}', {
        user_rec[0]}, ' {
        user_rec[1]}', {
        user_rec[4]});")
print("you have been billed successfully.")
else :
return 0

except:
print("error")


#admin only
def display_all(uid):
try:
inp = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|    tables:                                                     |
|----------------------------------------------------------------|
|        1] user                                                 |
|        2] plans                                                |
|        3] bill                                                 |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|

display table no:     """)
dct = {
        "1": "user",
        "2": "plans",
        "3": "bill"
}

cur.execute(f"select * from {
        dct[inp]};")
h = ["user id","username","account level","plan","plancost","phoneno","address","password"]
table = [h,] + cur.fetchall()
print(tabulate(table))

except:
print("error")


def god_mode(uid):
cur.execute(f"select account_lvl from user where uid = {
        uid
};")
if cur.fetchall()[0][0] == "I":
return 0
else :
command = input("enter mysql update command:\n")
try:
cur.execute(f" {
        command
}")
print("data updated.")
except:
print("error")

try:
print(cur.fetchall())
except:
pass




#log in
def log_in(uid):
try:
cur.execute(f"select name from user where uid = {
        uid
};")
print(f"Welcome back {
        cur.fetchone()[0]}")
cur.execute(f"select account_lvl from user where uid = {
        uid
};")

if cur.fetchone()[0] == "I":

while True:
b = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|----------------------------------------------------------------|
|    1] see your gym information                                 |
|    2] change plan                                              |
|    3] print bill                                               |
|    4] logout                                                   |
|    5] delete account                                           |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
        """)
if b == "1":
cur.execute(f"select * from user where uid = {
        uid
};")
h = ["user id","username","account level","plan","plancost","phoneno","address","password"]
table2 = [h,cur.fetchone()]
print(tabulate(table2))
elif b == "2":
change_plan(uid)
elif b == "3":
bill(uid)
elif b == "4":
break
elif b == "5":
del_account(uid)
else :
print("invalid input")

else :

while True:
b = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|----------------------------------------------------------------|
|    1] see your gym information                                 |
|    2] change your plan.                                        |
|    3] print bill                                               |
|    4] see all gym members's information                        |
|    5] update any record                                        |
|    6] delete any record                                        |
|    7] logout                                                   |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
        """)
if b == "1":
cur.execute(f"select * from user where uid = {
        uid
};")

h = ["user id","username","account level","plan","plancost","phoneno","address","password"]
table2 = [h,cur.fetchone()]
print(tabulate(table2))
elif b == "2":
change_plan(uid)
elif b == "3":
bill(uid)
elif b == "4":
display_all(uid)
elif b == "5":
god_mode(uid)
elif b == "6":
del_account(uid)
elif b == "7":
break
else :
print("invalid input")
cur.fetchall()
except:

print('error')


while True:
inp = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|    MENU:                                                       |
|----------------------------------------------------------------|
|        1] log in                                               |
|        2] new account                                          |
|        3] exit                                                 |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
        """)
try:
if inp == "1":
username = input("username: ")
password = input("password: ")
cur.execute(f"select count(uid), uid from user where name = ' {
        username
}' and password = ' {
        encrypt(password)}';")
rec = cur.fetchone()
if rec[0] == 0:
print("incorrect details.")
continue
else :
log_in(rec[1])


elif inp == "2":
new_account()

elif inp == "3":
break

else :
print("invalid input")

except:
print('error')
print("thank you")


conn.commit()
cur.close()
conn.close()