clauses = 0

R = [1,2,3]
A = [0,1,2,3,4]

T = dict()
H = dict()
ts = 1

ncl = 0

with open("vars.txt", "w+") as f:
    for i in R:
        for a in A:
            globals()[f"T_{i}_{a}"] = ts
            T[(i,a)] = ts
            f.write(f"v {ts} T_{i}_{a}\n")
            ts += 1
    # helper variables
    ws = ["ok", "win"]
    ws += ["a", "A", "b", "B", "c", "C"]

    for a in A:
        for a_ in A:
            if a != a_:
                ws += [f"ok_{a}_{a_}"]

    for w in ws:
        H[w] = ts
        f.write(f"v {ts} {w}\n")
        ts += 1



def c(literals):
    global cl
    literals = map(str, literals)
    cl.append((" ".join(literals)) + " 0")


qs = []
cl = []

# literals of first round
lits = []
for a in A:
    lits.append(str(T[(1,a)]))
qs.append("e " + (" ".join(lits)) + " 0")

# literals of second round

lits = []
for a in A:
    lits.append(str(T[(2,a)]))

# debug 
#(set to true to force one set of variables for the enemy round
# mind that if you set round of the enemy, the first player will most likely (and is allowed to) choose the same field.
#this is possible because in the real formula all second turns have to be true
if False: 
    qs.append("e " + (" ".join(lits)) + " 0")
    c([-T[2,0]])
    c([-T[2,1]])
    c([-T[2,2]])
    c([-T[2,3]])
    c([T[2,4]])
else:
    qs.append("a " + (" ".join(lits)) + " 0")

# literals of third round
lits = []
for a in A:
    lits.append(str(T[(3,a)]))
qs.append("e " + (" ".join(lits)) + " 0")


qs.append("e " + (" ".join(map(str, H.values()))) + " 0")


# at most one per turn in round 1
for a in A:
    for a_ in A:
        if a != a_:
            c([ -T[(1, a)], -T[(1, a_)] ])


# "forall possible assignments" contains wrong assignments.
# since either way we consider all assignments we don't need to check for stupid assignments
# like overlapping and no assignments (since these only make the game easier for x)
# We only have to check if the assignment is at most 1


cs = []
for a in A:
    for a_ in A:
        if a != a_:
            # ok if in every pair, one is not set
            # ok -> -t2_a or -t2_a'
            c([-H[f"ok_{a}_{a_}"], -T[(2,a)], -T[(2,a_)]])

            #? backimplication neccessary?
            # wrong
            c([H[f"ok_{a}_{a_}"], T[(2,a)]])
            c([H[f"ok_{a}_{a_}"], T[(2,a_)]])

            # ok -> all ok_a_a' are ok, too
            c([-H["ok"], H[f"ok_{a}_{a_}"]])
            cs.append(-H[f"ok_{a}_{a_}"])

cs.append(H["ok"])
c(cs)


# its okay if turn 2 is on top of turn 1
# so this constraint is left out
# ...

# we only check if round three is not on top of turn 2
for a in A:
    c([ -T[(2, a)], -T[(3, a)]])

# at most one per turn in round 3
for a in A:
    for a_ in A:
        if a != a_:
            c([ -T[(3, a)], -T[(3, a_)] ])



def win(f1, f2, w):
    c([-w, f1])
    c([-w, f2])

# winning?
# if enemy has his 
win(T[1,0], T[3,4], H["a"])
win(T[1,4], T[3,0], H["A"])
win(T[1,1], T[3,3], H["b"])
win(T[1,3], T[3,1], H["B"])
win(T[1,3], T[3,4], H["c"])
win(T[1,4], T[3,3], H["C"])

# win -> at least one winning row
c([-H["win"], H["a"], H["A"], H["b"], H["B"], H["c"], H["C"]])

# either we win or field is wrong
c([H["win"], -H["ok"]])

# comment in to check what happens if the deny the only two possinle winning strategies or one of it
#c([-H["B"]])
#c([-H["A"]])



print(f"p cnf {len(T)+len(H)} {clauses}")
print("\n".join(qs))
print("\n".join(cl))
