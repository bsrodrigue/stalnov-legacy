rns:
	python manage.py runserver

delmigrations:
	find . -path "*/migrations/*.py" -exec rm {} \;

delpyc:
	find . -name "*.pyc" -exec rm {} \;

mkmigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

test:
	python manage.py test
