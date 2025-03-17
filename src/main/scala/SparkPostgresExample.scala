// Create SparkSession
import org.apache.spark.sql.{DataFrame, DataFrameReader, SparkSession}
import org.apache.spark.sql.functions.{col, sum}

import java.util.Properties

object SparkPostgresExample {
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder
      // .master("local[*]")
      .appName("sparkpg")
      .getOrCreate()

    // Setup connection to database
    val dbConnection: DataFrameReader = (spark.read
      .format("jdbc")
      .option("url","jdbc:postgresql://postgres/postgres")
      .option("user","user")
      .option("password","password")
      .option("driver","org.postgresql.Driver")
      )

    // Read orders and user information
    val orders: DataFrame = dbConnection.option("dbtable","orders").load()
    val users: DataFrame = dbConnection.option("dbtable","users").load()
    // Read info regarding product availability and costs
    val products: DataFrame = dbConnection.option("dbtable","products").load()

    // Add product info to the orders table
    val orders_with_price = orders.join(products, products("id") === orders("product_id"))
    orders_with_price.cache()

    //
    val properties = new Properties()
    properties.setProperty("user","user")
    properties.setProperty("password","password")
    properties.setProperty("driver","org.postgresql.Driver")


    // Get total money spent and quantity per item per day
    orders_with_price.groupBy(orders("created_at"),products("id"),products("name")).agg(sum("quantity").as("order_quantity"), sum("price").as("order_spent")).write.mode("overwrite").jdbc("jdbc:postgresql://postgres/postgres", "report", properties)


  }
}