from datetime import date
import logging
import pickle
import pandas as pd
import numpy as np

logging.basicConfig(filename='predict_logs.txt',
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('predict_Logger')
log.setLevel(logging.INFO)


class Predict:
    def __init__(self):
        self.median_diff = 230951.0
        self.model_file_path = 'xgbmodel.pkl'
        self.x_preprocess_file_path = 'x_preprocess.pkl'
        self.y_preprocess_file_path = 'y_scaler.pkl'

    def predict(self, data):
        car_data = self.extract_features(data)
        car_data = self.preprocess(car_data)
        price = self.predict_price(car_data)
        price = self.transform_price(price)
        return price

    def extract_features(self, data):
        response = [int(data['kilometers']), data['owner'], data['fuel'], data['transmission'], float(data['condition'])]
        if data['current_price'] == '0':
            response.append(float(data['current_price']) + self.median_diff)
        else:
            response.append(float(data['current_price']))
        year = date.today().year
        response.append(year - int(data['year']))
        response.append(int(data['insurance']))
        if data['current_price'] == '0':
            response.append(1)
        else:
            response.append(0)
        log.info('Data format done.')
        log.info(response)
        return response

    def preprocess(self, data):
        try:
            with open(self.x_preprocess_file_path, 'rb') as f:
                preprocess_pipeline = pickle.load(f)
            log.info('Preprocessing pipeline loaded')
        except IOError as e:
            log.error('Error in loading preprocess model')
        data = np.array(data).reshape(1, -1)
        df = pd.DataFrame(data, columns=['Kilometers Driven', 'Owner', 'Fuel Type',
       'Transmission', 'Car Condition', 'Current Price', 'Age',
       'Insurance_Expired', 'No_Current_Price'])
        data = preprocess_pipeline.transform(df)
        log.info('Data is preprocessed.')
        return data

    def predict_price(self, car_data):
        try:
            with open(self.model_file_path, 'rb') as f:
                model = pickle.load(f)
            log.info('XGBoost model is loaded')
        except IOError as e:
            log.error('Error in loading XGBoost model.')

        price = model.predict(car_data)
        log.info('Prediction done.')
        return price

    def transform_price(self, price):
        try:
            with open(self.y_preprocess_file_path, 'rb') as f:
                sc_y = pickle.load(f)
            log.info('Y standard scaler loaded')
        except IOError as e:
            log.error('Error in loading standard scaler model.')

        price = sc_y.inverse_transform([price])
        log.info('Inverse transform done.')
        return price

