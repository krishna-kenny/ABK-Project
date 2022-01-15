#local_info.csv has all data except password.
#password.dat has passwords in binary
#table in local_info.csv: | serial no. | username | account level | number of machines | monthly charge |

import csv, pickle as p
with open('local_info.csv', "r") as f:
    gym = list(csv.reader(f))

def find(username, gym = gym):
    n = 0
    while n < len(gym):        
        if gym[n][1] == username:
            sno = gym[n][0]
            return gym[n]
        n+=1    
    return False      

def new_account(username, password, gym = gym):
    
    new = 0
    gym.append([len(gym), username, "I", int(new), 100*int(new)])    
    while True:
        new = input("Number of machines per day [we have max of 50]: ")
        if float(new) > 0 and float(new) <= 50 and float(new) == int(new):
            find(username)[3] = int(new)
            charge = 100*int(new)
            print(f"Your monthly charge is {charge}")
            break
        elif new == "exit":
            break
        else:
            print("* invalid value *")

    
    with open("password.dat", "ab") as fb:
        p.dump(password, fb)


def log_in(username):
    global gym 
    print(f"Welcome back {username}")

    if find(username)[2] == "I":
        
        while True:
            b = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|                                                                |
|    1] see your gym information                                 |
|                                                                |
|    2] change number of machines                                |
|                                                                |
|    3] logout                                                   |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
""")
            if b == "1":
                print("| serial no. | username | account level | number of machines | monthly charge |")
                print(find(username))
            elif b == "2":                
                machines = find(username)[3]
                print(f"* current amount of machines is {machines} *")

                while True:
                    new = input(" New number of machines per day [we have max of 50]: ")
                    if float(new) > 0 and float(new) <= 50 and float(new) == int(new):
                        rec = find(username)
                        rec[3] = int(new)
                        rec[4] = 100*int(new)
                        charge = 100*int(new)

                        gym[int(rec[0])] = rec
                        print(f"* new value added successfully. new monthly charge is {charge} *")
                        break
                    elif new == "exit":
                        break
                    else:
                        print("* invalid value *")
                        
            elif b == "3":
                print("* thank you *")
                break
            elif b == "exit":
                    break
            else:
                print("* invalid input *")
        
    elif find(username)[2] == "II":
        while True:
            b = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|                                                                |
|    1] see all members gym information                          |
|                                                                |
|    2] Update your Membership plan                              |
|                                                                |
|    3] logout                                                   |
|                                                                |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
""")
            if b == "1":
                print("| serial no. | username | account level | number of machines | monthly charge |")
                for rec in gym:
                    print(rec)
            elif b == "3":
                print("* thank you *")
                break
            elif b == "exit":
                    break
            elif b == '2':
                 Plan = int(input('''
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|                                                                |
|  1] Daily Plan (₹2,000/-)                                      |
|                                                                |
|  2] Weekly Plan (₹5,000/-)                                     |
|                                                                |
|  3] Monthly Plan (₹20,000/-)                                   |
|                                                                |
|  4] Yearly Plan (₹70,000/-)                                    |
|                                                                |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
'''))
                 if Plan == 1:
                     print('* Your Membership plan has been updated to the Daily plan. *')
                 elif Plan == 2:
                     print('* Your Membership plan has been updated to the Weekly Plan. *')
                 elif Plan == 3:
                     print('* Your Membership plan has been updated to the Monthly Plan. *')
                 elif Plan == 4:
                     print('* Your Membership plan has been updated to the Yearly Plan. *')
                 else:
                     print('** Please choose one of the 4 membership plans. **')
            
            else:
                print("* invalid input *")

    else:
        return False
    


def inp():
    global gym 
    while True:
        a = input("""
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
|                           MENU                                 |
|           [Enter serial no. of option to select it]            |
|                                                                |
|    1] log in                                                   |
|                                                                |
|    2] sign up                                                  |
|                                                                |
|    3] exit [enter "exit" at any point to reach here]           |
|                                                                |
|                                                                |
|-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X|
""")

        if a == "1":
            while True:
                print("")
                username = input("Enter username: ")

                if find(username) != False:                    
                    password = input("Enter password: ")

                    with open("password.dat", "rb") as f:
                        for line in range(int(find(username)[0])):                 
                            t = p.load(f)
                        if password == p.load(f):
                            log_in(username)
                            break
                        elif password == "exit":
                            break
                        else:
                            print("* incorrect password *")
                elif username == "exit":
                    break
                else:
                    print(f"* no user with username: {username} *")

        elif a == "2":
            username = input("Enter username [password or username cannot be changed]: ")
            password = input("Enter password: ")

            if username == "exit" or password == "exit":
                break
            elif find(username) == False:
                print("* New account created *")
                new_account(username, password)                            
            else:
                print("* Account with this username already exists *")
       
        elif a == "3" or "exit":
            print("* thank you *")
            break
        
        else:
            print("* invalid input *")

inp()
with open("local_info.csv", "w") as f:
    csv.writer(f).writerows(gym)
