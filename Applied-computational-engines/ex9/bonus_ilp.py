
# tiles
M = list("abcdefghi")
T = list(map(str,list(range(1,9+1))))
LR = [(1,2), (2,3), (4,5), (5,6), (7,8), (8,9)]
UD = [(1,4), (2,5), (3,6), (4,7), (5,8), (6,9)]


# weights
W = dict()

f = open("Bremen/lrud.txt", "r").readlines()
for l in f:
    l = l.strip()

    # weight, from a, to b, direction
    w, a, b, d = l.split(" ")
    a = a.replace(".png", "")
    b = b.replace(".png", "")

    if d == "LR":
        W[("LR",a,b)] = w

    if d == "UD":
        W[("UD",a,b)] = w



# variables
# t1_a t1_b ....


obj = []
for m1 in M:
    for m2 in M:
        if m1 != m2:
            w = W[("UD", m1, m2)]
            obj.append(f"{w}*xUD_{m1}_{m2}")
            w = W[("LR", m1, m2)]
            obj.append(f"{w}*xLR_{m1}_{m2}")

print("min: " + (" ".join(obj)) + ";")


# every tile has one map
for t in T:
    l = " ".join([f"1*x{t}_{m}" for m in M])
    print(f"{l} = 1;")

for m in M:
    l = " ".join([f"1*x{t}_{m}" for t in T])
    print(f"{l} = 1;")

# every tile has one map

for (t1, t2) in LR:
    for m1 in M:
        for m2 in M:
            if m1 != m2:
                print(f"1*x{t1}_{m1} 1*x{t2}_{m2} -1*xLR_{m1}_{m2} <= 1;")

for (t1, t2) in UD:
    for m1 in M:
        for m2 in M:
            if m1 != m2:
                print(f"1*x{t1}_{m1} 1*x{t2}_{m2} -1*xUD_{m1}_{m2} <= 1;")

for t in T:
    for m in M:
        print(f"1*x{t}_{m} <= 1;")

for m1 in M:
    for m2 in M:
        if m1 != m2:
            print(f"1*xUD_{m1}_{m2} <= 1;")
            
for t in T:
    for m in M:
        print(f"int x{t}_{m};")

for m1 in M:
    for m2 in M:
        if m1 != m2:
            print(f"int xUD_{m1}_{m2};")
