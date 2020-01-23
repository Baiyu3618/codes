main.o: main.f08
	gfortran -c main.f08
run.exe: main.o
	gfortran main.o -o run.exe
run: run.exe
	./run.exe
clean:
	rm *.o *.exe 
