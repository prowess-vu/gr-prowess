.PHONY : all debug clean

all : clean
	cmake -DCMAKE_BUILD_TYPE=Release -B build
	cmake --build build
	sudo cmake --install build

debug : clean
	cmake -DCMAKE_BUILD_TYPE=Debug -B build
	cmake --build build
	sudo cmake --install build

clean :
	rm -rf build

run :
	sudo cset shield --userset=prowess --exec -- python3 apps/run_flowgraph.py --pipes=10 --stages=10 --config=diamond
