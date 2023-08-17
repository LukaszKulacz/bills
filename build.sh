echo "Building the project..."
pip install -r requirements.txt

echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput