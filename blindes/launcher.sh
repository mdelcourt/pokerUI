cd files/
rm sponsor_folder/.kill_change_sponsor
python files/sponsor_folder/change.py &
./blindes.out
touch sponsor_folder/.kill_change_sponsor
cd -