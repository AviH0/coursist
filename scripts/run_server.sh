source env/bin/activate

echo "Killing server..."
pkill -f runserver

echo "Starting server..."
python manage.py runserver 0.0.0.0:5000 >>console.log 2>&1 &
echo "Server is running"
echo ""

tail -n 0 -f console.log
