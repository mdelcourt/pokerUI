cd files/
rm sponsor_folder/.kill_change_sponsor
cd sponsor_folder
python change.py &
cd ..
./blindes.out
touch sponsor_folder/.kill_change_sponsor
cd ..
