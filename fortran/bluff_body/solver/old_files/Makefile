# this is the makefile for bluff body computation
parameters.o: parameters.f08
	gfortran -c parameters.f08
initializer.o: initializer.f08 parameters.o
	gfortran -c initializer.f08
main.o: main.f08 parameters.o initializer.o
	gfortran -c main.f08
post_computer.o: post_computer.f08 parameters.o initializer.o solver.o
	gfortran -c post_computer.f08
solver.o: solver.f08 parameters.o initializer.o
	gfortran -c solver.f08
run.exe: main.o parameters.o initializer.o post_computer.o solver.o
	gfortran *.f08 -o run.exe
run: run.exe
	./run.exe
clean:
	rm *.o *.exe *.mod
