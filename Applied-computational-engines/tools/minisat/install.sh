DIR=$PWD
cd /tmp
wget http://minisat.se/downloads/minisat-2.2.0.tar.gz
tar -xvzf minisat-2.2.0.tar.gz
cd minisat
export MROOT=/tmp/minisat
cd simp
make
cp minisat $DIR
