
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


variables = ["a", "b", "c", "g1", "g2", "g3", "g4", "o"]
variables += ["g1'", "g2'", "g3'", "g4'", "g5'", "o'"]

x = dict()
i = 0
for v in variables:
    i += 1
    x[v] = str(i)




def op_not(v1,out):
    clause(f"{x[v1]} {x[out]}")
    clause(f"-{x[v1]} -{x[out]}")

def op_and(v1,v2,out):
    clause(f"{x[v1]} {x[v2]} -{x[out]}")
    clause(f"{x[v1]} -{x[v2]} -{x[out]}")
    clause(f"-{x[v1]} {x[v2]} -{x[out]}")
    clause(f"-{x[v1]} -{x[v2]} {x[out]}")

def op_or(v1,v2,out):
    clause(f"{x[v1]} {x[v2]} -{x[out]}")
    clause(f"{x[v1]} -{x[v2]} {x[out]}")
    clause(f"-{x[v1]} {x[v2]} {x[out]}")
    clause(f"-{x[v1]} -{x[v2]} {x[out]}")

def op_xor(v1,v2,out):
    clause(f"{x[v1]} {x[v2]} {x[out]}")
    clause(f"{x[v1]} -{x[v2]} -{x[out]}")
    clause(f"-{x[v1]} {x[v2]} -{x[out]}")
    clause(f"-{x[v1]} -{x[v2]} {x[out]}")

def op_neq(v1,v2):
    clause(f"-{x[v1]} -{x[v2]}")
    clause(f"{x[v1]} {x[v2]}")

op_not("a", "g1")
op_not("b", "g2")
op_and("b", "c", "g3")
op_and("b", "c", "g4")
op_or("g2", "g4", "o")


op_and("a", "b", "g1'")
op_or("a", "c", "g3'")
op_or("b", "c", "g2'")
op_not("g2'", "g4'")
op_or("g4'", "g3'", "g5'")
op_xor("g1'", "g5'", "o'")


## o and o' differ
op_neq("o", "o'")

# printing variables
for c in variables:
    comment(f"{x[c]} = {c}")


print(f"p cnf {len(x)} {num_clauses}")
print("\n".join(lines))

