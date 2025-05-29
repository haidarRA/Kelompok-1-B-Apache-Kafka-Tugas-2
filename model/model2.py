from pyspark.sql import SparkSession
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pathlib import Path

#predict bitcoin high and low
spark = SparkSession.builder.appName("BitcoinHighLowPrediction").getOrCreate()

data_dir = Path(__file__).resolve().parent.parent / 'data' / 'batch' / 'batch_2.csv'
model_high_dir = Path(__file__).resolve().parent.parent / 'model' / 'model2_high'
model_low_dir = Path(__file__).resolve().parent.parent / 'model' / 'model2_low'

df = spark.read.csv(str(data_dir), header=True, inferSchema=True)
df = df.select("Open", "Volume", "High", "Low").dropna()

assembler = VectorAssembler(inputCols=["Open", "Volume"], outputCol="features")

rf_high = RandomForestRegressor(featuresCol="features", labelCol="High", predictionCol="High_pred")
rf_low = RandomForestRegressor(featuresCol="features", labelCol="Low", predictionCol="Low_pred")

features_df = assembler.transform(df)

model_high = rf_high.fit(features_df)
model_high.save(str(model_high_dir))

model_low = rf_low.fit(features_df)
model_low.save(str(model_low_dir))
