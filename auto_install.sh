chmod +x pokerUI.py
echo "*** Checking dependencies"
sudo apt-get update
sudo apt-get install g++ libsdl-ttf2.0-dev libsdl1.2-dev python-tk libsdl-image1.2-dev python2.7
cd blindes/files
chmod +x ../launcher.sh
chmod +x compile.sh
echo "*** Compiling program"
./compile.sh
chmod +x places.sh
echo "*** Done"
cd -
