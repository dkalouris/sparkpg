# Part 1: Adding Base Spark

Set up Apache Spark as the foundation for the project.

## How to run
To start all components run: 

```$docker compose up```

and to stop them:

```$docker compose down```

For running a service individually e.g. spark-master:

```$docker compose up spark-master```

To connect to the attach the terminal of your container to yours and execute commands while the service is running e.g. for spark-master: 

```$docker exec -it spark-master /bin/bash```

There are examples located inside spark, that you use can use for testing the UI for example for scala:
- Find code examples and the class names to reference in /opt/spark/examples/src/main/scala/org/apache/spark/examples 
- Submit them by using the jar /opt/spark/examples/jars/spark-examples_2.12-3.5.4.jar (exact jar path may vary based on spark installation)

Example run localy with 1 executor:  
```markdown 
spark-submit \
    --class org.apache.spark.examples.AccumulatorMetricsTest \
    --master local[1]  \
    /opt/spark/examples/jars/spark-examples_2.12-3.5.4.jar
```

Example run on Spark standalone cluster in client deploy mode:
```markdown 
spark-submit \
    --class org.apache.spark.examples.AccumulatorMetricsTest \
    --master spark://spark-master:7077 \
    --executor-memory 8G \
    --total-executor-cores 2 \
    /opt/spark/examples/jars/spark-examples_2.12-3.5.4.jar
```


### Useful links: 

- Spark master web UI url (contains info about spark master and connected executors): http://localhost:8080/
- Spark spark Web UI url (up only during job runs): http://localhost:4040/
- Spark history server url (contains completed job runs): http://localhost:18080/
