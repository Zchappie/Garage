NAME="code_tictactoe_07_rohloff_meng_abushanab"
ZIP="$NAME.zip"
rm $ZIP

zip -r $ZIP make.sh make_qbf.py vars.txt

unzip -l $ZIP
