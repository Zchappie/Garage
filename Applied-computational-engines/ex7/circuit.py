import itertools

lines = []
num_clauses = 0

# adds a clause to the output
def clause(c):
    global num_clauses, lines
    lines.append(c + " 0")
    num_clauses += 1

# adds a comment to the output
def comment(c):
    global num_clauses, lines
    lines.append("c " + c)


def swap(x1,x2,y1,y2):
    #x1 = lower in
    #x2 = upper in
    #y1 = lower out
    #y2 = upper out
    clause(f"-{x[x1]} {x[y2]}")
    clause(f"-{x[y1]} {x[x1]}")
    clause(f"-{x[x1]} {x[x2]} -{x[y1]} -{x[y2]}")
    clause(f"-{x[x1]} -{x[x2]} {x[y1]} -{x[y2]}")
    clause(f"{x[x1]} -{x[x2]} {x[y1]} {x[y2]}")
    clause(f"{x[x1]} {x[x2]} {x[y1]} -{x[y2]}")



variables = []
for i in range(1,18+1):
    variables += ["y"+str(i)]

variables += ["x0", "x1", "x2", "x3", "x4", "x5"]
variables += ["x0_", "x1_", "x2_", "x3_", "x4_", "x5_"]


x = dict()
i = 0
for v in variables:
    i += 1
    x[v] = str(i)

# first circuit
swap("x1", "x2", "y1", "y2")
swap("x4", "x5", "y3", "y4")
swap("x0", "y2", "y5", "y6")
swap("x3", "y4", "y7", "y8")
swap("y5", "y1", "y9", "y10")
swap("y7", "y3", "y11", "y12")
swap("y6", "y11", "y13", "y14")
swap("y9", "y14", "x0_", "y15")
swap("y10", "y12", "y16", "y17")
swap("y13", "y17", "y18", "x4_")
swap("y16", "y15", "x1_", "x3_")
swap("y18", "y8", "x2_", "x5_")


x1,x2,x3,x4,x5 = x["x1"], x["x2"], x["x3"], x["x4"], x["x5"]
clause(f"{x1} {x2} {x3} {x4} {x5}")
clause(f"{x1} {x2} {x3} {x4} -{x5}")
clause(f"{x1} {x2} {x3} -{x4} -{x5}")
clause(f"{x1} {x2} -{x3} -{x4} -{x5}")
clause(f"{x1} -{x2} -{x3} -{x4} -{x5}")
clause(f"-{x1} -{x2} -{x3} -{x4} -{x5}")


# printing variables
for c in variables:
    comment(f"{x[c]} = {c}")

print(f"p cnf {len(x)} {num_clauses}")
print("\n".join(lines))

