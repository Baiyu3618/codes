##############################################
# makefile for compilation of mesh generator #
##############################################

parameters.o: parameters.f08
	gfortran -c parameters.f08
subroutines.o: subroutines.f08 parameters.o params.mod model_vars.mod
	gfortran -c subroutines.f08
main.o: main.f08 params.mod model_vars.mod subroutines.o
	gfortran -c main.f08
run.exe: main.o
	gfortran *.o -o run.exe
run: run.exe
	./run.exe
clean:
	rm *.o *.mod *.exe
plot:
	python3 plotter.py
