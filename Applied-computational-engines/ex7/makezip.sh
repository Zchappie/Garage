NAME="07_rohloff_meng_abushanab"
ZIP="$NAME.zip"
rm $ZIP

zip -r $ZIP circuit.py make_qbf.py alloy.lp

PDF="$NAME.pdf"
pdflatex main.tex
cp main.pdf $PDF
zip -r $ZIP fabric.py $PDF

unzip -l $ZIP
