import sys

def lp():
    A = (2.8, 4.8);
    B = (3.8, 2.0);
    C = (1.8, 1.0);
    D = (2.7, 2.2);


    print(f"max: 1*y ;")

    (x1,y1),(x2,y2) = (A,B)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x <= {y1*(x2-x1)-x1*(y2 - y1)};")

    (x1,y1),(x2,y2) = (C,B)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x >= {y1*(x2-x1)-x1*(y2 - y1)};")

    (x1,y1),(x2,y2) = (C,D)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x <= {y1*(x2-x1)-x1*(y2 - y1)};")

    (x1,y1),(x2,y2) = (D,A)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x <= {y1*(x2-x1)-x1*(y2 - y1)};")

    
    print(f"x >= 0;")
    print(f"y >= 0;")


def ilp():
    A = (2.8, 4.8);
    B = (3.8, 2.0);
    C = (1.8, 1.0);
    #C = (0.8, 0.0); # uncomment to add an additional minumum for x and y
    D = (2.7, 2.2);

    E = []
    E.append((B,A))
    E.append((C,B))
    E.append((C,D))
    E.append((A,D))


    print(f"max: 1*y ;")

    (x1,y1),(x2,y2) = (A,B)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x <= {y1*(x2-x1)-x1*(y2 - y1)};")

    (x1,y1),(x2,y2) = (C,B)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x >= {y1*(x2-x1)-x1*(y2 - y1)};")

    (x1,y1),(x2,y2) = (C,D)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x -99999*o1 <= {y1*(x2-x1)-x1*(y2 - y1)};")

    (x1,y1),(x2,y2) = (D,A)
    print(f"{x2-x1}*y {-1*(y2-y1)}*x -99999*o2 <= {y1*(x2-x1)-x1*(y2 - y1)};")

    
    print(f"1*o1 1*o2 < 1;")
    print(f"x >= 0;")
    print(f"y >= 0;")
    print(f"o1 <= 1;")
    print(f"o2 <= 1;")
    print(f"int y;")
    print(f"int x;")
    print(f"int o1;")
    print(f"int o2;")


if __name__ == "__main__":
    if sys.argv[1] == "lp":
        lp()
    if sys.argv[1] == "ilp":
        ilp()
