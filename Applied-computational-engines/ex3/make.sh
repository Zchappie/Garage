NAME="03b_rohloff_meng_tschubij"
ZIP="$NAME.zip"
rm $ZIP

zip -r $ZIP cnfs/.gitignore
zip -r $ZIP benchmarks/06_*
zip -r $ZIP Examples/.gitignore
zip -r $ZIP fabric.py fabric_debug.py benchmark.py

PDF="$NAME.pdf"
pdflatex main.tex
cp main.pdf $PDF
zip -r $ZIP fabric.py $PDF

unzip -l $ZIP
