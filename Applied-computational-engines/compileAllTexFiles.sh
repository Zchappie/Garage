COMPILE="*.tex"
DICTS="*/"

shopt -s nullglob

function diffpdf(){
    REV=$2
    if [ -z "$2" ]; then REV="HEAD~"; fi;
    git show $REV:./$1 > "$1.old"
    cmp --silent $1.old $1 || latexdiff "$1.old" $1 > $1.diff.tex
}



for dir in $DICTS; do
    cd $dir
    for file in $COMPILE; do
        diffpdf "$file"
    done
    for file in $COMPILE; do
        echo $file
        latexmk -e '$pdflatex=q/pdflatex -synctex=1 -interaction=nonstopmode/' -pdf "$file" -f
    done
    rm *.tex.old
    rm *.diff.tex
    cd ..
done
