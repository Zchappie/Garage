
# tiles
M = list("abcdefghi")
T = list(map(str,list(range(1,9+1))))
LR = [(1,2), (2,3), (4,5), (5,6), (7,8), (8,9)]
UD = [(1,4), (2,5), (3,6), (4,7), (5,8), (6,9)]


with open("vars.txt", "w+") as variables:

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

