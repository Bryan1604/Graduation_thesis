build:
	docker-compose -f docker_compose_spark.yml build
build-nc:
	docker-compose -f docker_compose_spark.yml build --no-cache 
build-progress:
	docker-compose -f docker_compose_spark.yml build --no-cache progress=plain
down:
	docker-compose down --volumes
run:
	make down && docker-compose -f docker_compose_spark.yml up

run-scaled:
	make down && docker-compose -f docker_compose_spark.yml up --scale spark-worker=3

run-d:
	make down && docker-compose -f docker_compose_spark.yml up -d
stop:
	docker-compose -f docker_compose_spark.yml stop

submit:
	docker exec spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./app/$(app)