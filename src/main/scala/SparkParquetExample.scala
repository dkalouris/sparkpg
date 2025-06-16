import org.apache.spark.sql.{DataFrame, SparkSession}

object SparkParquetExample {
  def main(args: Array[String]): Unit = {
    if (args.length < 1) {
      println("Usage: SparkParquetExample <output_directory>")
      System.exit(1)
    }

    val outputDir: String = args.mkString("")
    println(outputDir)
    val spark: SparkSession = SparkSession.builder
      .appName("sparkParquet")
      .getOrCreate()

    // Read data and print
    import spark.implicits._
    val data : DataFrame = Seq( (1,"name1") , (2,"name2") ).toDF("id","name")
    data.write.mode("overwrite").parquet(outputDir.concat("/example_parquet_folder"))

  }
}