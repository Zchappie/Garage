from pprint import pprint
from fabric import * 
import pycosat

f = Fabric()
w, h, shapes, connections, blocks = f.parse_input(sys.argv[1])
X, cnf = f.fabric(w, h, shapes, connections)
solution = pycosat.solve(cnf)

print(solution)
print("h", h)
print("w", w)

print("Shapes/Tiles:")
pprint(shapes)
print("Connections:")
pprint(connections)

f.print_shapes(blocks)


if solution == "UNSAT":
    print("UNSAT")
else:
    img = [list("."*(w+2)) for i in range(h)]

    for y in range(0,h):
        for x in range(0,w+2):
            img[y][x] = " "

    for (c, tile), i in X.items():
        if X[(c,tile)] in solution:
            (x,y) = c
            if img[y][x] != " ":
                img[y][x] = "E"
            else:
                img[y][x] = str(tile[0])


    print(np.array(img))


