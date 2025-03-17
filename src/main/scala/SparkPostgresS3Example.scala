import org.apache.spark.sql.{DataFrame, DataFrameReader, SparkSession}

object SparkPostgresS3Example {
  def main(args: Array[String]): Unit = {

    val spark: SparkSession = SparkSession.builder
      .appName("sparkS3")
      .getOrCreate()

    // Setup connection to database
    val dbConnection: DataFrameReader = (spark.read
      .format("jdbc")
      .option("url","jdbc:postgresql://postgres/postgres")
      .option("user","user")
      .option("password","password")
      .option("driver","org.postgresql.Driver")
      )

    // Read orders data from database
    val orders: DataFrame = dbConnection.option("dbtable","orders").load()

    // Write to S3
    orders.write.mode("overwrite").parquet("s3a://bucket1/orders_parquet")
  }
}