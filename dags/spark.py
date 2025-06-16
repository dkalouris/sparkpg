from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG(
    dag_id = "spark",
    start_date = datetime(2025,1,1),
    schedule_interval = None,
    catchup = False,
    concurrency=2,
    default_args = {"retries" : 0}
) as dag:

    emptyop = EmptyOperator(task_id="test_task")

    accumulator_metrics = SparkSubmitOperator(
        task_id = "AccumulatorMetricsClient",
        application = "/home/sparkuser/spark/examples/jars/spark-examples_2.12-3.5.6.jar",
        conn_id = "spark_standalone_client",
        java_class='org.apache.spark.examples.AccumulatorMetricsTest',
        executor_cores=2,
        total_executor_cores=2,
        verbose=True
    )

    spark_parquet = SparkSubmitOperator(
        task_id = "SparkParquetExampleClient",
        application = "/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id = "spark_standalone_client",
        java_class='SparkParquetExample',
        application_args=['file:///app/output/'],
        executor_cores=2,
        total_executor_cores=2,
        verbose=True
    )

    spark_s3 = SparkSubmitOperator(
        task_id = "SparkS3ExampleClient",
        application = "/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id = "spark_standalone_client",
        java_class='SparkS3Example',
        executor_cores=2,
        total_executor_cores=2,
        verbose=True
    )

    spark_postgres = SparkSubmitOperator(
        task_id = "SparkPostgresExampleClient",
        application = "/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id = "spark_standalone_client",
        java_class='SparkPostgresExample',
        executor_cores=2,
        total_executor_cores=2,
        verbose=True
    )

    spark_s3_postgres = SparkSubmitOperator(
        task_id = "SparkPostgresS3ExampleClient",
        application = "/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id = "spark_standalone_client",
        java_class='SparkPostgresS3Example',
        executor_cores=2,
        total_executor_cores=2,
        verbose=True
    )
    
    

