import org.apache.spark.sql.{DataFrame, SparkSession}
object SparkS3Example {
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder
      .appName("sparkS3")
      .getOrCreate()

    // Read data and print
    val data : DataFrame = spark.read.option("header","true").csv("s3a://bucket1/sample.csv")
    data.write.mode("overwrite").parquet("s3a://bucket1/sample_parquet")

  }
}