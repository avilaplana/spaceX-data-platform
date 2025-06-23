.PHONY: build run logs

# Build the ETL image
build:
	docker build --no-cache -t etl-without-airflow:latest -f Dockerfile ..	

# Run the services with environment variables
run:
	export $$(cat database.env | xargs) && docker compose up -d

# View ETL service logs
logs:
	docker compose logs -f etl 

# Stop and remove all the containers
stop:
	docker compose down

# Stop all services and remove volumes
clean:
	docker compose down -v 	