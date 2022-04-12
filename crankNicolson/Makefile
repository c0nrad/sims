run: build
	time ./crankNicolson

profile:
	g++ -std=c++11 --coverage -fprofile-arcs -I ./extern/eigen-3.4.0/ main.cpp -o crankNicolson	
	./crankNicolson
	gcov main.cpp

build:
	g++ -std=c++11   -I ./extern/eigen-3.4.0/ main.cpp -o crankNicolson