
lines = []
num_clauses = 0

def clause(c):
    global num_clauses, lines
    lines.append(c + " 0")
    num_clauses += 1

def comment(c):
    global num_clauses, lines
    lines.append("c " + c)


vertices = [1,2,3,4,5,6,7,8,9,10]
colors = [1,2,3]
E = [(1,3),(3,5),(5,2),(2,4),(4,1),
    (6,10),(10,9),(9,8),(8,7),(7,6),
    (1,6),(5,10),(4,9),(3,8),(2,7)]

# Define a relation from x_v_c to numbers
i = 0
x = dict()
for (v1,v2) in E:
    for c in colors:
        i += 1
        x[(v1,v2,c)] = str(i)

comment("Contraint 1")
for (v1,v2) in E:
    cl = []
    for c in colors:
        cl.append(x[(v1,v2,c)])
    comment(f"({v1},{v2}) has at least one color")
    clause(" ".join(cl))

comment("Contraint 2")
for c1 in colors:
    for c2 in colors:
        if c1 != c2:
            for (v1,v2) in E:
                comment(f"({v1},{v2} is not both {c1} and {c2}")
                clause(f"-{x[(v1,v2,c1)]} -{x[(v1,v2,c2)]}")

comment("Contraint 3")
for v1, v2 in E:
    for v3, v4 in E:
        if v1==v3 or v1==v4 or v2==v3 or v2==v4:
            for c in colors:
                comment(f"c{c} not on ({v1},{v2}) or (v3,v4)")
                clause(f"-{x[(v1,v2,c)]} -{x[v3,v4,c]}")

comment(f"Variable meanings:")
for (v1,v2) in E:
    for c in colors:
        comment(f"if {x[v1,v2,c]} then x_{v1}_{v2}_{c} => (x{v1}, x{v2}) is of color {c}")

print(f"p cnf {len(E)*len(colors)} {num_clauses}")
print("\n".join(lines))

