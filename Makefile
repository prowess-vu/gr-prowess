all :
	rm -rf build
	cmake -DCMAKE_BUILD_TYPE=Release -B build
	cmake --build build
	cmake --install build

debug :
	rm -rf build
	cmake -DCMAKE_BUILD_TYPE=Debug -B build
	cmake --build build
	cmake --install build

clean :
	rm -rf build
