rm *.mod *.o run
gfortran -c parameters.f08
gfortran -c *.f08
gfortran *.o -o run
./run
python3 plotter.py
