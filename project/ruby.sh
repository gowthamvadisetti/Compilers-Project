make clean;
make;
bin/irgen $1;
make codegen;
make spim;