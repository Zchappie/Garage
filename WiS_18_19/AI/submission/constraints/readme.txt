CHILDREN is a domain, contains all 8 children denoted by intergers from 1 to 8.
Each child has an ID following the order of their names, in the following solution explainations, I
will also use the first letter to refer the corresponding child.

GAMES is a domain, contains 4 games denoted by intergers from 1 to 4.
1 is Risk; 2 is Scrabble, 3 is UNO, 4 is Lego.

SET is a domain, contains 2 states denoted by 1 and 0.
Means whether choose the refering game or not.

I set a matrix quiet[i,j] = k.
Means child with i-th ID, plays the game j if k=1;
otherwise child with i-th ID, doesn't play the game j.

SOLUTIONS:
2.1-No solution found!


2.2-
[[1, 0, 0, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[1, 0, 0, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 1, 0, 0;int(1..4)], 
[0, 1, 0, 0;int(1..4)], 
[1, 0, 0, 0;int(1..4)];int(1..8)]
A plays Risk; B plays UNO,; C plays Risk; D plays Lego;
E plays UNO; F plays Scrabble; G plays Scrabble; H plays Risks

2.3-No solution found!

2.4-
[[0, 0, 0, 1;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)];int(1..8)]
A, F, H play Lego; B, C, D, E, G play UNO

2.5-
[[1, 0, 0, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[1, 0, 0, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)], 
[1, 0, 0, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)];int(1..8)]
A, C, G play Risk; B, E play UNO; D, F, H play Lego

2.6-
[[0, 0, 1, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)], 
[0, 0, 1, 0;int(1..4)], 
[0, 0, 0, 1;int(1..4)];int(1..8)]
A, B, D, E, G paly UNO; C, F, H play Lego
