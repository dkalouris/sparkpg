# Spark + postgreSQL + Minio + Airflow  Tutorial

![Architecture Diagram: This diagram illustrates the system architecture of the project. It features PostgreSQL as the storage database, Apache Spark for data processing and execution, and MinIO for object storage. Apache Airflow is used for scheduling tasks. All services are orchestrated and run locally using Docker Compose, providing a seamless development environment.](images/architecture_diagram.png)

## Overview

Welcome to Spark Data Stack Tutorial! This project aims to setup Apache Spark integration with other technologies using only docker-compose. These can help as first step for diving into Spark and exploring its capabilities or they can be used for other projects, as part of unit tests or deployed as is for local testing. 
It will be developed in multiple phases, progressively adding new features and capabilities. 

If you`re interested in a step by step guide on how each service was added you can follow this [reading list](https://medium.com/@dkalouris/list/modern-spark-data-stack-using-dockercompose-81c0bff6e3ef) on Medium.

## How to run

### Using docker-compose
To start all components run:

```$docker compose up```

and to stop them:

```$docker compose down```

For running a service individually e.g. spark-master:

```$docker compose up spark-master```

To connect to the attach the terminal of your container to yours and execute commands while the service is running e.g. for spark-master:

```$docker exec -it spark-master /bin/bash```

### Compiling code to jar:
Run docker `docker compose up jar-builder` (running all services can be resource intensive, it is good idea to run this ahead of starting the other services.)

By default jar-builder will run `sbt assembly` creating a fat jar with the base classes and all the dependencies mentioned in `build.sbt` (postgresql, minio).

If you want to create a jar including only the base classes and no external dependencies change jar-builder to execute `sbt package` instead.

### Submitting jar to Spark cluster:

To submit fat jar created using sbt-assembly use:

for Parquet example:
```markdown 
spark-submit \
    --class SparkParquetExample \
    --master spark://spark-master:7077 \
    --executor-memory 8G  \
    --total-executor-cores 2 \
    target/scala-2.12/sparkpg-assembly-1.0.jar \
    output
```

for PostgreSQL example:
```markdown 
spark-submit \
    --class SparkPostgresExample \
    --master spark://spark-master:7077 \
    --executor-memory 8G  \
    --total-executor-cores 2 \
    target/scala-2.12/sparkpg-assembly-1.0.jar
```
for S3 example:

```markdown 
spark-submit \
    --class SparkS3Example \
    --master spark://spark-master:7077 \
    --executor-memory 8G  \
    --total-executor-cores 2 \
    target/scala-2.12/sparkpg-assembly-1.0.jar
```
for postgres + s3 example:

```markdown 
spark-submit \
    --class SparkPostgresS3Example \
    --master spark://spark-master:7077 \
    --executor-memory 8G  \
    --total-executor-cores 2 \
    target/scala-2.12/sparkpg-assembly-1.0.jar
```
There are also examples located inside spark, that you use can use for testing the UI for example for scala:
- Find code examples and the class names to reference in /home/sparkuser/spark/examples/src/main/scala/org/apache/spark/examples
- Submit them by using the jar /home/sparkuser/spark/examples/jars/spark-examples_2.12-3.5.5.jar (exact jar path may vary based on spark installation)


Example run localy with 1 executor:
```markdown 
spark-submit \
    --class org.apache.spark.examples.AccumulatorMetricsTest \
    --master local[1]  \
    /home/sparkuser/spark/examples/jars/spark-examples_2.12-3.5.5.jar
```

Example run on Spark standalone cluster in client deploy mode:
```markdown 
spark-submit \
    --class org.apache.spark.examples.AccumulatorMetricsTest \
    --master spark://spark-master:7077 \
    --executor-memory 8G \
    --total-executor-cores 2 \
/home/sparkuser/spark/examples/jars/spark-examples_2.12-3.5.5.jar
```
Running jobs using Airflow:
- Once services are up and running navigate to [airflow web url](http://localhost:8090/)
- Click on "DAGS" and find dag named "spark"
- Click on trigger button to start execution
- You can view running jobs Spark master web UI url

![Airflow web UI url layout for dag named "spark". Provides a clear overview of the DAG's structure and the status of its tasks at a glance. All tasks are empty, the DAG is not running and there are no scheduled tasks. On the top right there is a red rectacle indicator to indicate the position where the trigger button is located.](images/airflow_trigger.png)

### Useful links:

- Spark master web UI url (contains info about spark master and connected executors): http://localhost:8080/
- Spark spark web UI url (up only during job runs): http://localhost:4040/
- Spark history server url (contains completed job runs): http://localhost:18080/
- pgadmin4 url (GUI for viewing postgresql): http://localhost:8050/
- airflow web UI url: http://localhost:8090/

## Changelog

### Part 1: Adding Base Spark

Set up Apache Spark as the foundation for the project.

Configured the initial Spark environment for data processing and added the relevant Dockerfile and README files.

### Part 2: Integration with a relational databases (PostgreSQL)

Renamed and moved code to root

Updates:
- Dockerfile: added postgresql jar and installation for sbt
- docker-compose.yaml: added postgres and pgadmin services and added sparkpg repo as bind mount to spark-master
- Added sbt assembly support by adding [build.sbt](build.sbt) and [plugins.sbt](project/plugins.sbt) files
- Created [init file](init.sql) and [new class example]([src/main/scala/SparkPostgresExample) to test the database

### Part 3: Adding Object Storage (Minio)

Updates:
- Dockerfile & build.sbt: added aws related jars 
- docker-compose.yaml: added minio and  mc services
- policy.json: new s3 policy example
- init-minio.sh: bash commands needed to initialize new user and attach permissions using mc
- spark-defaults.conf: updated with credentials and address for minio
- Two new classes [S3]([src/main/scala/SparkS3Example) and [Postgres+S3]([src/main/scala/SparkPostgresS3Example) to test the new code

### Part 4: Adding Scheduling (Airflow)

Updates:
- [Dockerfile.airflow](Dockerfile.airflow): added to extend base airflow image
- docker-compose.yaml: added jar-builder service and airflow related services
- [.env](.env): added with environment variables for airflow services
- [APACHE-LICENCE](APACHE-LICENCE): added as part of using snippets as a base for airflow services in docker compose that were licensed under the same terms
- Aiflow [example dag](/dags/spark.py) added


## Next Steps
That's all wrapped up for now! I hope you found this Docker Compose setup useful. If you have any suggestions for improvements, additional features, or enhancements, I would love to hear from you. Please feel free to open an issue or submit a pull request!

## License

This project is licensed under both the [Apache License 2.0](APACHE-LICENCE) and the [MIT License](LICENCE). You must comply with the terms of both licenses when using, modifying, or distributing this project.

### Summary

- **MIT License**: Allows you to do almost anything with the software, as long as you include the original copyright and license notice.

- **Apache License 2.0**: Allows you to use, modify, and distribute the software, but requires you to include a copy of the license and provide attribution.