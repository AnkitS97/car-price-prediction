import pandas as pd
from datetime import date
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from pickle import dump
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import logging

logging.basicConfig(filename='training_logs.txt',
                            filemode='a',
                            format='%(asctime)s %(levelname)s-%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('train_Logger')
log.setLevel(logging.INFO)

class TrainModel:

    def __init__(self, car_data_path, models_data_path):
        self.med_diff = 0
        self.car_data_path = car_data_path
        self.models_data_path = models_data_path

    def train(self):
        log.info('Training started')
        df = self.merge_data(self.car_data_path, self.models_data_path)
        df = self.clean_data(df)
        x = df.drop(['Selling Price'], axis=1)
        y = df.loc[:, 'Selling Price']
        x = self.preprocess_X(x)
        y = self.preprocess_y(y)
        model = XGBRegressor(learning_rate=0.1,
                             n_estimators=100,
                             max_depth=6,
                             min_child_weight=6,
                             gamma=0.2,
                             subsample=0.85,
                             colsample_bytree=0.85)
        log.info('XGBoost model training started')
        model.fit(x, y)
        error = mean_squared_error(y, model.predict(x))
        log.info('XGBoost model training finished with MSE of ' + str(error))
        try:
            dump(model, open('xgbmodel.pkl', 'wb'))
            log.info('XGBoost model saved successfully')
        except IOError as e:
            log.error('Error in saving XGBoost model')

    def merge_data(self, car_data_path, models_data_path):
        car_df = pd.read_csv(car_data_path)
        model_df = pd.read_csv(models_data_path)

        df = pd.merge(car_df, model_df, left_on='Model', right_on='Model')
        log.info('Merged the two datasets')
        return df

    def clean_data(self, df):
        df['Current Price'] = df['Current Price'].apply(self.format_price)
        df[df['Current Price'] == 'nan'] = 0
        df['Current Price'] = df['Current Price'].astype(int)
        log.info('Cleaned Current Price Feature')
        year = date.today().year
        df['Age'] = year - df['Year']
        log.info('Added Age Feature')
        df = df[df['Selling Price'] != 0]
        df['Transmission'] = df['Transmission'].apply(self.clean_transmission)
        log.info('Cleaned Transmission Feature')
        mode_imputer = SimpleImputer(strategy="most_frequent")
        df['Insurance'] = mode_imputer.fit_transform(df['Insurance'].values.reshape(-1, 1))
        df['Insurance_Expired'] = 0
        df.loc[df['Insurance'] == 'Expired', 'Insurance_Expired'] = 1
        log.info('Added Insurance Expired Feature')
        df['No_Current_Price'] = 0
        df.loc[df['Current Price'] == 0, 'No_Current_Price'] = 1
        df['diff'] = df['Current Price'] - df['Selling Price']
        self.med_diff = df[df['diff'] > 0]['diff'].median()
        log.info('Median difference between current price and selling price is ' + str(self.med_diff))
        df.loc[:, 'Current Price'] = df.apply(self.set_current_price, axis=1)
        df.drop(['Model', 'Year', 'Insurance', 'diff'], axis=1, inplace=True)
        log.info('Data Cleaned')
        return df

    def preprocess_X(self, x):
        num_attribs = ['Kilometers Driven', 'Car Condition', 'Current Price', 'Age']
        cat_attribs = ['Owner', 'Fuel Type', 'Transmission']
        preprocessing = ColumnTransformer([
            ("num", StandardScaler(), num_attribs),
            ("cat", OneHotEncoder(drop='first', sparse=False), cat_attribs)
        ], remainder="passthrough")
        x = preprocessing.fit_transform(x)
        log.info('Preprocessed X features')
        try:
            dump(preprocessing, open('x_preprocess.pkl', 'wb'))
            log.info('Saved x preprocessing model')
        except IOError as e:
            log.error('Error in saving Independent features preprocessing model')
        return x

    def preprocess_y(self, y):
        sc_y = StandardScaler()
        y = sc_y.fit_transform(y.values.reshape(-1, 1))
        try:
            dump(sc_y, open('y_scaler.pkl', 'wb'))
            log.info('Saved y preprocessing model')
        except IOError as e:
            log.error('Error in saving y preprocess model')
        return y

    def format_price(self, price):
        price = str(price)
        price = price.replace('Rs.', '')
        price = price.replace(',', '')
        num_zeros = 5
        if '.' not in price and ' Lakh' in price:
            price = price.replace(' Lakh', '0' * num_zeros)
        elif '.' in price and ' Lakh in price':
            n = len(price)
            m = price.index('.')
            num_zeros = n - m - num_zeros
            price = price.replace(' Lakh', '0' * num_zeros)
            price = price.replace('.', '')
        return price

    def clean_transmission(self, trans):
        if 'MANUAL' != trans and 'AUTOMATIC' != trans:
            trans = "MANUAL"
        return trans

    def set_current_price(self, row):
        if row['Current Price'] == 0 or row['diff'] < 0:
            row['Current Price'] = row['Selling Price'] + self.med_diff

        return row['Current Price']
