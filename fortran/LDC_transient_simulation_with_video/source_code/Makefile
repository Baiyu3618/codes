# this is the make file for lde problem
parameters.o: parameters.f08
	gfortran -c parameters.f08
initializer.o: parameters.o params.mod model_vars.mod
	gfortran -c initializer.f08
main.o: main.f08 params.mod model_vars.mod
	gfortran -c main.f08
solvers.o: solvers.f08 params.mod model_vars.mod
	gfortran -c solvers.f08
run.exe: main.o parameters.o solvers.o initializer.o params.mod model_vars.mod
	gfortran *.o -o run.exe
run: run.exe
	./run.exe
clean:
	rm -rf *.o *.mod *.exe velocity_contour pressure_contour
