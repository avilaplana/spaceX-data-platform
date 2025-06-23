# Build the Airflow image
build:
	docker build --no-cache -t etl-airflow:latest -f Dockerfile ..

# Run the services with environment variables
run:
	export $$(cat database.env | xargs) && docker compose up -d

# View Airflow webserver logs
logs:
	docker compose logs -f airflow-webserver

# View Airflow scheduler logs
scheduler-logs:
	docker compose logs -f airflow-scheduler

# View all logs
all-logs:
	docker compose logs -f

# Stop all services
stop:
	docker compose down

# Stop all services and remove volumes
clean:
	docker compose down -v 