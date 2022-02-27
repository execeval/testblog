web: gunicorn testblog-app.wsgi --log-file --log-level debug
python manage.py makemigrations
python manage.py migrate
python manage.py runserver