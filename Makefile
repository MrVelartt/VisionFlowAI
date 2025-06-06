project:
	docker compose run --rm web django-admin startproject $(PROJECT_NAME) .

app:
	docker compose run --rm web ./manage.py startapp $(APP_NAME)

delete-celery:
	rm -f src/celeryev.pid

up:
	docker compose up --remove-orphans

run:
	rm -f src/celeryev.pid
	docker compose up -d

build:
	docker compose build

clean:
	#rm -rf src/*/migrations/00**.py
	find . -name "*.pyc" -exec rm -- {} +
	rm -rf src/*/migrations/__pycache__/*

reset:
	docker compose down -v
	rm -rf ./postgres/.pgdata

delete-messages:
	rm -rf src/locale/en/
	rm -rf src/locale/es/
	rm -rf src/*/locale/en/
	rm -rf src/*/locale/es/

django:
	docker compose restart web

migrate:
	docker compose run --rm web python manage.py makemigrations
	docker compose run --rm web python manage.py migrate

statics:
	docker compose run --rm web python manage.py collectstatic --no-input

superuser:
	docker compose run --rm web python manage.py createsuperuser

test:
	docker compose run --rm web python manage.py test --no-input --parallel

flake:
	docker compose run --rm web flake8

stop:
	docker compose stop


messages:
	docker compose run --rm web python manage.py makemessages -l 'es'
	docker compose run --rm web python manage.py makemessages -l 'en'

compilemessages:
	docker compose run --rm web python manage.py compilemessages -f

coverage:
	docker compose run --rm web coverage erase
	docker compose run --rm web coverage run ./manage.py test
	docker compose run --rm web coverage report

coverage-html:
	docker compose run --rm web coverage html

generate-pylint:
	docker compose run --rm web pylint --generate-rcfile > .pylintrc

pylint:
	docker compose run --rm web bash -c './pylint.sh'

bash:
	docker compose run --rm web bash

pylint-partial:
	docker compose exec -T web pylint $(PATH_FILES)

update-component:
	docker compose exec web python manage.py update_presentation_product

restart:
	docker compose restart django