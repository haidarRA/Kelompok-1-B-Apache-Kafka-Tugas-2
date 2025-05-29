from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pathlib import Path

#predict bitcoin trend
spark = SparkSession.builder.appName("BitcoinTrendPrediction").getOrCreate()

data_dir = Path(__file__).resolve().parent.parent / 'data' / 'batch' / 'batch_1.csv'
model_dir = Path(__file__).resolve().parent.parent / 'model' / 'model3'

df = spark.read.csv(str(data_dir), header=True, inferSchema=True)
df = df.select("Open", "Close", "Volume").dropna()

df = df.withColumn("label", when(df["Close"] > df["Open"], 1).otherwise(0))
assembler = VectorAssembler(inputCols=["Open", "Close", "Volume"], outputCol="features")

features_df = assembler.transform(df).select("features", "label")

lr = LogisticRegression(featuresCol="features", labelCol="label", predictionCol="prediction", regParam=0.1)

model = lr.fit(features_df)
model.save(str(model_dir))