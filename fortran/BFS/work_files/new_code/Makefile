main.o: main.f08 params.mod model_vars.mod initializer.o subroutines1.o subroutines2.o subroutines3.o
	gfortran -c main.f08
parameters.o: parameters.f08
	gfortran -c parameters.f08
initializer.o: initializer.f08
	gfortran -c initializer.f08
subroutines1.o: subroutines1.f08
	gfortran -c subroutines1.f08
subroutines2.o: subroutines2.f08
	gfortran -c subroutines2.f08
subroutines3.o: subroutines3.f08
	gfortran -c subroutines3.f08
run.exe: main.o parameters.o
	gfortran *.o -o run.exe
run: run.exe
	./run.exe
clean:
	rm *.o *.mod *.exe
