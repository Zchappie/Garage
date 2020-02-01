DIR=$PWD
cd /tmp
wget https://github.com/lonsing/depqbf/archive/version-5.0.tar.gz
tar -xvzf version-5.0.tar.gz
cd depqbf-version-5.0
make
cp depqbf $DIR
