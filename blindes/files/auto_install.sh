echo "*** Checking dependencies"
sudo apt-get install gcc g++ libsdl-ttf2.0-0 libsdl-ttf2.0-dev libsdl1.2-dev python3 xterm
chmod +x launcher.sh
cp launcher.sh ../
rm blindes.out
echo "*** Compiling program"
g++ main.cpp `sdl-config --libs --cflags ` -lSDL_ttf -o blindes.out
chmod +x places.sh
chmod +x ../launcher.sh
echo "*** Done"