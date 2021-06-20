redis-server &
echo "ok"
python3 main.py &>m.txt
python3 recv.py &>r.txt
bin/www &
sleep 300
