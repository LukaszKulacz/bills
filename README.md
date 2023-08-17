# Bills
Aplikacja pozwalająca na zarządzanie wynajmowanymi pokojami.

### Instalacja

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py runserver
```


### Użyteczne polecenia

```bash
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
python manage.py test
python manage.py makemigrations bills
python manage.py migrate
python manage.py createsuperuser
````
