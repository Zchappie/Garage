DIR=$PWD
cd /tmp
wget http://fmv.jku.at/picosat/picosat-960.tar.gz
tar -xvzf picosat-960.tar.gz
cd picosat-960
./configure
make
cp picosat $DIR
