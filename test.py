import pickle as p

with open("password.dat", "ab") as f:
    p.dump("k", f)

"""with open("password.dat", "rb") as f:
    try:
        while True:
            print(p.load(f))
    except:
        print("Done")"""