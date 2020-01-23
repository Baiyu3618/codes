thermal_solver.o: thermal_solver.f08 thermal_parameters.o thermal_subroutines1.o thermal_subroutines2.o
	gfortran -c thermal_solver.f08
thermal_parameters.o: thermal_parameters.f08
	gfortran -c thermal_parameters.f08
thermal_subroutines1.o: thermal_subroutines1.f08
	gfortran -c thermal_subroutines1.f08
thermal_subroutines2.o: thermal_subroutines2.f08
	gfortran -c thermal_subroutines2.f08
clean:
	rm *.mod *.o *.exe Data.csv
run.exe: thermal_solver.o
	gfortran *.o -o run.exe
run: run.exe
	./run.exe
