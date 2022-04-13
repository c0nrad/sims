run: build
	time ./crankNicolson

build:
	g++ -std=c++11 -I ./extern/eigen-3.4.0/ main.cpp -o crankNicolson

plot: build
	./crankNicolson > data.data
	gnuplot -p -e "plot 'data.data'"

plot-gif: build
	./crankNicolson > data.data
	gnuplot gif.gnu
	open foobar.gif
