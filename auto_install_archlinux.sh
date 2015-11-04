chmod +x pokerUI.py
echo "*** Checking dependencies"
sudo pacman -S  gcc tk sdl sdl_tff python2
cd blindes/files
chmod +x ../launcher.sh
chmod +x compile.sh
echo "*** Compiling program"
./compile.sh
chmod +x places.sh
echo "*** Done"
cd -
