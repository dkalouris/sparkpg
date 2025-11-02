from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import re

def read_spark_version(**kwargs):
    filepath = "/home/sparkuser/spark/RELEASE"
    with open(filepath, 'r') as file:
        data = file.read()
        match = re.search(r"Spark 3\.5\.(\d+)", data)
        if match:
            version = f"3.5.{match.group(1)}"
            kwargs['ti'].xcom_push(key="spark_version", value=version)
            print(f"Spark version extracted: {version}")
        else:
            raise ValueError("No Spark version found in RELEASE")

## Note: If you`re not able to edit this file execute chown user:user dags/spark.py but make sure you have id 1000 for airflow to work
with DAG(
    dag_id="spark",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    concurrency=2,
    default_args={"retries": 0},
) as dag:

    emptyop = EmptyOperator(task_id="test_task")

    accumulator_metrics = SparkSubmitOperator(
        task_id="AccumulatorMetricsClient",
        application="{{ '/home/sparkuser/spark/examples/jars/spark-examples_2.12-' ~ ti.xcom_pull(task_ids='get_spark_version', key='spark_version') ~ '.jar' }}",
        conn_id="spark_standalone_client",
        java_class="org.apache.spark.examples.AccumulatorMetricsTest",
        executor_cores=2,
        total_executor_cores=2,
        verbose=True,
    )
    
    get_spark_version = PythonOperator(
        task_id='get_spark_version',
        python_callable=read_spark_version,
        provide_context=True
    )

    get_spark_version >> accumulator_metrics

    ## Note: if all tasks afterv this fail its possible the jar is not generated so execute 'docker compose up jar-builder' to assemble it
    spark_parquet = SparkSubmitOperator(
        task_id="SparkParquetExampleClient",
        application="/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id="spark_standalone_client",
        java_class="SparkParquetExample",
        application_args=["file:///app/output/"],
        executor_cores=2,
        total_executor_cores=2,
        verbose=True,
    )

    spark_s3 = SparkSubmitOperator(
        task_id="SparkS3ExampleClient",
        application="/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id="spark_standalone_client",
        java_class="SparkS3Example",
        executor_cores=2,
        total_executor_cores=2,
        verbose=True,
    )

    spark_postgres = SparkSubmitOperator(
        task_id="SparkPostgresExampleClient",
        application="/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id="spark_standalone_client",
        java_class="SparkPostgresExample",
        executor_cores=2,
        total_executor_cores=2,
        verbose=True,
    )

    spark_s3_postgres = SparkSubmitOperator(
        task_id="SparkPostgresS3ExampleClient",
        application="/app/target/scala-2.12/sparkpg-assembly-1.0.jar",
        conn_id="spark_standalone_client",
        java_class="SparkPostgresS3Example",
        executor_cores=2,
        total_executor_cores=2,
        verbose=True,
    )
    get_spark_version >> []
