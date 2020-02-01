B=$(wc -l <(bash replace_edges.sh | grep "*" -vh | grep "min" -vh) | cut -d" " -f1)
echo "* #variable= 27 #constraint= $((A+B))"
bash replace_edges.sh
#cat static.txt
#cat edges.txt
