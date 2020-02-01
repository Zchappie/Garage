
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


vertices = [1,2,3,4,5,6,7,8,9,10]
colors = [1,2,3]
E = [
        (1,3), (3,5), (5,2), (2,4), (4,1),
        (6,10), (10,9), (9,8), (8,7), (7,6),
        (1,6), (5,10), (4,9), (3,8), (2,7),
        ]




# creating a dictionary to associate (x_vc) to numbers
i = 0
x = dict()
for v in vertices:
    for c in colors:
        i += 1
        x[(v,c)] = str(i)





# adding constraints

comment("Contraint 1 - Every Vertex has at least one color")
for v in vertices:
    cl = []
    for c in colors:
        cl.append(x[(v,c)])

    clause(" ".join(cl)) # join makes a string out of the numbers and places spaces between the numbers






# printing variables
for v in vertices:
    for c in colors:
        comment(f"{x[v,c]} is x_{v}_{c}")


print(f"p cnf 30 {num_clauses}")
print("\n".join(lines))

