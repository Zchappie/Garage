python make_qbf.py
python make_qbf.py | depqbf 
python make_qbf.py | depqbf --qdo

echo ""
echo "False:"
echo ""

python make_qbf.py | depqbf --qdo | grep "-" | cut -d" " -f2 | cut -d"-" -f2 | while read line; do
    grep "v $line " vars.txt
done

echo ""
echo "True:"
echo ""

python make_qbf.py | depqbf --qdo | grep -v "-" | cut -d" " -f2 | while read line; do
    grep "v $line " vars.txt
done
