name := "sparkpg"
version := "1.0"
libraryDependencies += "org.scala-lang" % "scala-library" % "2.12.0"

scalaVersion := "2.12.18"

val sparkVersion = "3.5.4"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion % "provided",
  "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",
  "org.postgresql" % "postgresql" % "42.7.4"
)