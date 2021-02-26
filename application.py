from flask import Flask, render_template, request
from flask_cors import cross_origin, CORS
from train import TrainModel
from predict import Predict

application = Flask(__name__)
CORS(application)


@application.route('/', methods=['GET'])
@cross_origin()
def home_page():
    return render_template('index.html', price=0)


@application.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    if request.form:
        prediction_model = Predict()
        car_data = request.form
        price = prediction_model.predict(car_data)
        return render_template('index.html', price=price[0][0])
    else:
        return render_template('index.html', price=0)


@application.route('/train', methods=['GET'])
@cross_origin()
def train_model():
    trainmodel = TrainModel('car_data.csv', 'model_data.csv')
    trainmodel.train()
    return 'Model Trained!'


if __name__ == '__main__':
    # for running on local machine
    application.run(port=8000)
    # Uncomment this for running on cloud
    # application.run()
