python3 petersen.py > petersen.cnf
python3 petersen_edge.py > petersen_edge.cnf
cat petersen.cnf | grep "Variable meanings" -A 100000 > petersen.vars
cat petersen_edge.cnf | grep "Variable meanings" -A 100000 > petersen_edge.vars
picosat petersen.cnf > petersen.solution
picosat petersen_edge.cnf > petersen_edge.solution
pdflatex main.tex

ZIP="rohloff_meng_tschubij.zip"
rm $ZIP
zip $ZIP petersen*.cnf petersen*.solution petersen*.py
cp main.pdf abgabe.pdf
zip $ZIP abgabe.pdf


