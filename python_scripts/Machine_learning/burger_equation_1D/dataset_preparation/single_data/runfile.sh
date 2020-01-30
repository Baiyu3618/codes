rm *.csv
gfortran -c main.f08
gfortran main.o -o run.exe
./run.exe
rm *.o *.exe
