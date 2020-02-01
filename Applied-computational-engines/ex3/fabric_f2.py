import numpy as np
import sys
from copy import deepcopy

class Fabric:

    def __init__(self):
        self.lines = []
        self.num_clauses = 0
        self.clauses = []

    # adds a clause to the output
    def clause(self, *args):
        c = " ".join([str(x) for x in args])
        clause = c + " 0"
        self.lines.append(c + " 0")
        self.num_clauses += 1
        self.clauses.append(args)

    # adds a comment to the output
    def comment(self, c):
        self.lines.append("c " + c)

    # Rotates a given 2D-Array
    def rotate(self, array):
        arr1 = np.array(array)
        Y, X = arr1.shape
        # Element Length < 5! Be careful with large Problem instances.
        arr2 = np.zeros((X, Y), dtype="<U5")

        for y in range(Y):
            for x in range(X):
                nx = Y-y-1
                ny = x
                a = arr1[y][x]
                arr2[ny][nx] = a
        return arr2

    # Parses the input shapes. Copys and rotates them too.
    def parse_input(self, input_file):
        with open(input_file) as f:
            lines = f.readlines()
            w = lines[0]
            h = lines[1]
            lines = lines[3:]

            lines = [l.strip() for l in lines]
            lines = ",".join(lines)
            blocks = lines.split(",,")
            blocks = [[list(a) for a in t.split(",")] for t in blocks]
            blocks = [[b for b in a if len(b) > 0] for a in blocks if len(a) > 0]

            rot_1 = [self.rotate(a) for a in deepcopy(blocks)]
            rot_2 = [self.rotate(a) for a in deepcopy(rot_1)]
            rot_3 = [self.rotate(a) for a in deepcopy(rot_2)]
            rot_4 = [self.rotate(a) for a in deepcopy(rot_3)]

            tiles = []
            connections = []
            blocks = sum(map(list,zip(rot_1, rot_2, rot_3, rot_4)), [])

            # Replace + with a number in each shape
            for block_id, block in enumerate(blocks):
                tile_id = 0
                for y, row in enumerate(block):
                    for x, char in enumerate(row):
                        if char == "+":
                            tile_id += 1
                            blocks[block_id][y][x] = tile_id
                            t = (block_id, tile_id)
                            tiles.append(t)

            # build the connection graph between these numbers
            for block_id, block in enumerate(blocks):
                for y, row in enumerate(block):
                    for x, tile_id in enumerate(row):
                        if tile_id != ".":
                            tile_id = int(tile_id)
                            t1 = (block_id, tile_id)
                            for direction, x_, y_ in [("vertical", x,y+1), ("horizontal", x+1,y)]:
                                if y_ < len(block):
                                    if x_ < len(row):
                                        tile_id_ = block[y_][x_]
                                        if tile_id_ != ".":
                                            tile_id_ = int(tile_id_)
                                            t2 = (block_id, tile_id_)
                                            if direction == "vertical":
                                                connections.append((t1, "d", t2))
                                            if direction == "horizontal":
                                                connections.append((t1, "r", t2))

            # tiles is the needed for the cnf generation
            # blocks is a printable version of all shapes
            return int(w), int(h), tiles, connections, blocks

    def fabric(self, w, h, tiles, connections, output=True, into_file=None):
        self.lines = []
        self.num_clauses = 0
        self.clauses = []

        # define variables
        X = dict()
        O = []
        F = []
        i = 1

        # Area F1
        for x in range(1, w+1):
            for y in range(h):
                c = (x,y)
                F.append(c)
                for t in tiles:
                    X[(c, t)] = i
                    i += 1

        # Area O
        for y in range(h):
            c1 = (0, y)
            O.append(c1)
            F.append(c1)
            c2 = (w+1, y)
            O.append(c2)
            F.append(c2)
            for t in tiles:
                X[(c1, t)] = i
                i += 1
                X[(c2, t)] = i
                i += 1

        # Constraints
        self.comment("No border node has a tile")
        for c in O:
            for t in tiles:
                self.clause(-X[c,t])

        # self.comment("Every node has a tile")
        # for c in F1+F2:
        #     dis = []
        #     for t in tiles:
        #         self.comment(f"{c} {t}")
        #         dis.append(X[c,t])
        #     self.clause(*dis)

        # self.comment("Every node has at most one tile")
        # for c in F1+F2:
        #     for t1 in tiles:
        #         for t2 in tiles:
        #             if t1 != t2:
        #                 self.comment(f"{c} not {t1} and {t2}")
        #                 self.clause(-X[c,t1], -X[c,t2])

        self.comment("Ladder Encoding: Only one tile on each field")
        ladder_vars = 0
        for c in F:
            Y = []
            for t in tiles:
                Y.append(i) 
                i += 1

            t = tiles[0]
            self.clause(X[c,t], -Y[0])
            self.clause(-X[c,t], Y[0])

            for j in range(0, len(tiles) - 1):
                self.clause(Y[j+1], -X[c, tiles[j + 1]])
                self.clause(Y[j+1], -Y[j])
                self.clause(-Y[j+1], X[c, tiles[j + 1]], Y[j])
            
            self.clause(Y[len(tiles) - 1])

            for j in range(0, len(tiles) - 1):
                self.clause(-Y[j], -X[c, tiles[j + 1]])
            ladder_vars += len(Y)

        self.comment("Every set tile implies its neigbor tiles")
        A = set(F+O)
        for (x, y) in A:
            for s1, d, s2 in connections:
                c1 = (x, y)
                if d == "r": 
                    c2 = (x+1, y)
                    if c2 in A:
                        self.clause(-X[c1, s1], X[c2, s2])
                        self.clause(-X[c2, s2], X[c1, s1])
                        pass
                if d == "d": 
                    c2 = (x, (y+1) % h)
                    if c2 in A:
                        self.clause(-X[c1, s1], X[c2, s2])
                        self.clause(-X[c2, s2], X[c1, s1])
                        pass

        if output:
            print(f"p cnf {len(X)+ladder_vars} {self.num_clauses}")
            print("\n".join(self.lines))

        if into_file:
            with open(into_file, "w+") as file:
                file.write(f"p cnf {len(X)+ladder_vars} {self.num_clauses}\n")
                file.write("\n".join(self.lines))

        return X, self.clauses

    def print_shapes(self, blocks):
        for i, block in enumerate(blocks):
            print()
            print("Block:"+str(i)+":")
            for row in block:
                print("".join(row))

            print()


if __name__ == "__main__":
    f = Fabric()
    if len(sys.argv) == 2:
        w, h, tiles, connections, b = f.parse_input(sys.argv[1])
        X, cnf = f.fabric(w, h, tiles, connections)
    else:
        print("No input file!")

