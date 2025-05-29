from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pathlib import Path

#predict bitcoin close
spark = SparkSession.builder.appName("BitcoinPricePrediction").getOrCreate()

data_dir = Path(__file__).resolve().parent.parent / 'data' / 'batch' / 'batch_3.csv'
model_dir = Path(__file__).resolve().parent.parent / 'model' / 'model1'

df = spark.read.csv(str(data_dir), header=True, inferSchema=True)
df = df.select("Timestamp", "Close").dropna()

assembler = VectorAssembler(inputCols=["Timestamp"], outputCol="features")
data = assembler.transform(df).select("features", "Close")

lr = LinearRegression(featuresCol='features', labelCol='Close', predictionCol="Close_pred", regParam=0.1)
model = lr.fit(data)

model.save(str(model_dir))