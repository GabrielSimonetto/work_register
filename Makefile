install:
	poetry install
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run python manage.py loaddata time_register

run:
	poetry run python manage.py runserver 8080

docker_build:
	docker build . -t work_register

docker_run:
	docker run -d -p 8080:8080 work_register

test:
	poetry run pytest -s

shell:
	poetry run python manage.py shell
