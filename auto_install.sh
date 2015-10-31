echo "*** Checking dependencies"
sudo apt-get install g++ libsdl-ttf2.0-dev libsdl1.2-dev python-tk libsdl-image1.2-dev
cd blindes/files
chmod +x launcher.sh
cp launcher.sh ../
rm blindes.out
echo "*** Compiling program"
g++ main.cpp `sdl-config --libs --cflags ` -lSDL_ttf -lSDL_image -o blindes.out
chmod +x places.sh
chmod +x ../launcher.sh
echo "*** Done"
cd -
