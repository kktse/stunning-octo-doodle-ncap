PATHS = stunning-octo-doodle-ncap

install-dev:
	pip install -r requirements/development.txt

docker-up:
	docker-compose up
	
docker-start:
	docker-compose start

docker-stop:
	docker-compose stop
	
docker-down:
	docker-compose down

build:
	docker-compose build
	
migrate:
	docker-compose exec web python manage.py migrate

db-populate:
	docker-compose exec web python manage.py init_db

test:
	./stunning-octo-doodle-ncap/manage.py test ${PATHS}

lint:
	flake8 ${PATHS}