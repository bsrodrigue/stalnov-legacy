rns:
	python ./src/manage.py runserver

delmigrations:
	find ./src -path "*/migrations/*.py" -exec rm {} \;

delpyc:
	find ./src -name "*.pyc" -exec rm {} \;

mkmigrations:
	python ./src/manage.py makemigrations

migrate:
	python ./src/manage.py migrate

superuser:
	python ./src/manage.py createsuperuser

test:
	python ./src/manage.py test
