
# tiles
M = list("abcdefghijkl")
T = list(map(str,list(range(1,12+1))))
LR = [(1,2), (2,3), (3,4), 
        (5,6), (6,7), (7,8),
        (9,10), (10,11), (11,12)]

UD = [(1,5), (2,6), (3,7), (4,8),
        (5,9), (6,10), (7,11), (8,12)]


with open("vars_london.txt", "w+") as variables:

    X = dict()
    k = 1
    for t in T:
        for m in M:
            X[f"x{t}_{m}"] = f"x{k}"
            variables.write(f"x{t}_{m}  x{k}\n")
            k += 1

    for m1 in M:
        for m2 in M:
            if m1 != m2:
                X[f"xUD_{m1}_{m2}"] = f"x{k}"
                variables.write(f"xUD_{m1}_{m2}  x{k}\n")
                X[f"xLR_{m1}_{m2}"] = f"x{k}"
                variables.write(f"xLR_{m1}_{m2}  x{k}\n")
                k += 1


    lines = open("bonus.ilp", "r").readlines()

    o = []

    print(f"* #variable= 1037 #constraint= 1035")
    for l in lines:
        if not "int" in l:
            for k, v in X.items():
                l = l.replace(k,v)
            l = l.replace("*"," ")
            o.append(l)

    print("".join(o))

