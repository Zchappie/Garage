CNFS="liu_circuit circuit"
read -ra ADDR <<< "$CNFS"
for F in "${ADDR[@]}"; do
    python3 $F.py > $F.cnf
    cat $F.cnf | grep "Variable meanings" -A 100000 > $F.vars
    picosat $F.cnf > $F.solution
done

pdflatex main.tex
ZIP="02_rohloff_meng_tschubij.zip"
rm $ZIP
zip $ZIP liu*.cnf liu*.solution liu*.py
cp main.pdf abgabe.pdf
zip $ZIP abgabe.pdf
unzip -l $ZIP


