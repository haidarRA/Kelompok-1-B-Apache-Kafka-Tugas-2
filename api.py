from flask import Flask, request, jsonify
from pyspark.ml.regression import LinearRegressionModel, RandomForestRegressionModel
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
from pathlib import Path

app = Flask(__name__)
spark = SparkSession.builder.appName("BitcoinAPI").getOrCreate()

model1_dir = Path(__file__).resolve().parent / 'model' / 'model1'
model2_high_dir = Path(__file__).resolve().parent / 'model' / 'model2_high'
model2_low_dir = Path(__file__).resolve().parent / 'model' / 'model2_low'
model3_dir = Path(__file__).resolve().parent / 'model' / 'model3'

models = {
    "model1": LinearRegressionModel.load(str(model1_dir)),
    "model2_high": RandomForestRegressionModel.load(str(model2_high_dir)),
    "model2_low": RandomForestRegressionModel.load(str(model2_low_dir)),
    "model3": LogisticRegressionModel.load(str(model3_dir)),
}

@app.route('/predict/close', methods=['GET'])
def predict_model1():
    timestamp = int(request.args.get('timestamp'))
    
    df = spark.createDataFrame([(Vectors.dense([timestamp]),)], ["features"])

    pred_close = models["model1"].transform(df).collect()[0]['Close_pred']

    return jsonify({
        "timestamp": timestamp,
        "predicted_close": pred_close
    })

@app.route('/predict/high_low', methods=['GET'])
def predict_model2():
    open_val = float(request.args.get('open'))
    volume = float(request.args.get('volume'))
    
    df = spark.createDataFrame([(open_val, volume)], ["Open", "Volume"])
    assembler = VectorAssembler(inputCols=["Open", "Volume"], outputCol="features")
    features_df = assembler.transform(df)

    pred_high = models["model2_high"].transform(features_df).collect()[0]["High_pred"]
    pred_low = models["model2_low"].transform(features_df).collect()[0]["Low_pred"]

    return jsonify({
        "open": open_val,
        "volume": volume,
        "predicted_high": pred_high,
        "predicted_low": pred_low
    })

@app.route('/predict/trend', methods=['GET'])
def predict_model3():
    open_val = float(request.args.get('open'))
    close_val = float(request.args.get('close'))
    volume = float(request.args.get('volume'))

    df = spark.createDataFrame([(open_val, close_val, volume)], ["Open", "Close", "Volume"])
    assembler = VectorAssembler(inputCols=["Open", "Close", "Volume"], outputCol="features")
    features_df = assembler.transform(df)

    prediction = models["model3"].transform(features_df).collect()[0]["prediction"]

    trend = "Up" if prediction == 1.0 else "Down"
    return jsonify({
        "open": open_val,
        "close": close_val,
        "volume": volume,
        "predicted_trend": trend
    })


if __name__ == '__main__':
    app.run(port=5000)