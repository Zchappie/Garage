#assignment 2-1
#x, y are the inputs; z is output of the gate
def g_or(x, y, z):
    print(x, y, -z, 0)
    print(-x, z, 0)
    print(-y,z, 0)
def g_and(x, y, z):
    print(-x, -y, z, 0)
    print(x, -z, 0)
    print(y, -z, 0)
def g_not(x, z):
    print(-x, -z, 0)
    print(x, z, 0)
def g_xor(x, y, z):
    print(-x, -y, -z, 0)
    print(x, y, -z, 0)
    print(x, -y, z, 0)
    print(-x, y, z, 0)

#left one
#a, b, c, g1, g2, g3, g4, o = [1,2,3,4,5,6,7,8]
print("p cnf 14 33")    
g_not(1, 4)
g_not(2, 5)
g_and(2, 3, 6)
g_and(4, 6, 7)
g_or(5, 7, 8)    

#right one
#G1,G2,G3,G4,G5,O = [9,10,11,12,13,14]
g_and(1, 2, 9)
g_or(2, 3, 10)
g_or(1, 3, 11)
g_not(10, 12)
g_or(12, 11, 13)
g_xor(9, 13, 14)

#verify the equivlency
print(-8, -14, 0)
print(8, 14, 0)
