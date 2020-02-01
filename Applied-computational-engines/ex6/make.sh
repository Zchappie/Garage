bash run.sh > deutschland.opd
sat4j deutschland.opd

NAME="06_rohloff_meng_abushanab"
ZIP="$NAME.zip"
rm $ZIP

zip -r $ZIP deutschland.opd static.txt run.sh make.sh

PDF="$NAME.pdf"
pdflatex main.tex
cp main.pdf $PDF
zip -r $ZIP fabric.py $PDF

unzip -l $ZIP
