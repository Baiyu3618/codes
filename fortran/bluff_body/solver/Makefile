parameters.o: parameters.f08
	@gfortran -c parameters.f08

subroutines1.o: subroutines1.f08
	@gfortran -c subroutines1.f08

subroutines2.o: subroutines2.f08
	@gfortran -c subroutines2.f08

main.o: main.f08 params.mod model_vars.mod subroutines1.o subroutines2.o
	@gfortran -c main.f08

run.exe: main.o
	@gfortran *.o -o run.exe

run: run.exe
	@./run.exe

clean:
	@rm -f *.o *.exe *.mod *~ 

all: clean parameters.o subroutines1.o subroutines2.o main.o run.exe run 
