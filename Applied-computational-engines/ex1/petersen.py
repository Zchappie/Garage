
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
for v in vertices:
    for c in colors:
        i += 1
        x[(v,c)] = str(i)


comment("Contraint 1")
for v in vertices:
    cl = []
    for c in colors:
        cl.append(x[(v,c)])
    comment(f"x{v} has at least one color")
    clause(" ".join(cl))

comment("Contraint 2")
for c1 in colors:
    for c2 in colors:
        if c1 != c2:
            for v in vertices:
                comment(f"x{v} is not colored with both {c1} and {c2}")
                clause(f"-{x[(v,c1)]} -{x[(v,c2)]}")


comment("Contraint 3")
for v1, v2 in E:
    for c in colors:
        comment(f"c{c} not on x{v1} or x{v2}")
        clause(f"-{x[(v1,c)]} -{x[v2,c]}")

comment(f"Variable meanings:")
for v in vertices:
    for c in colors:
        comment(f"if {x[v,c]} then x_{v}_{c} => x{v} is of color {c}")

print(f"p cnf 30 {num_clauses}")
print("\n".join(lines))

