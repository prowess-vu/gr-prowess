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
