# Car Price Prediction

### **About:**
The main aim of this project was to help the users willing to buy a used car to estimate the approximate selling price of the car they are buying to make sure they are priced appropriately and not overpaying. This project also helps users selling their car to get an idea of what would be an appropriate price for their vehicle and then sell their car accordingly. The application takes various inputs from the user like car condition, distance covered by the car, transmission type. It then predicts an approximate price that might be ideal depending on the car conditions provided. 

### Images of Application

Landing page
![landing page](https://github.com/AnkitS97/car-price-prediction/blob/main/image1.PNG?raw=true)


Prediciton page
![prediction page](https://github.com/AnkitS97/car-price-prediction/blob/main/image2.PNG?raw=true)

### Features

- scrapper.py
  The scrapper.py file is used to scrapper data from various websites. Run the scrapper.py file to generate dataset by scrapping data from websites like [Car Dekho](https://www.cardekho.com/) and [Car Wale](https://www.carwale.com/).\
   It uses selenium to first extract urls of different vehicles available on used car selling websites and then it hits these urls iteratively to get the necessary inforamtion out    of it. At the end, it generates 2 csv files.

- car_data.csv
  It contains all the information about the features of the car.\
    - Model: Model name of the car that is sold.
    - Selling Price: The selling price of the car. This is your target feature.
    - Kilometers Driven: Number of kilometers that the car has already driven.
    - Year: Year of purchase of the car.
    - Owner: Information on a number of the previous owners.
    - Fuel Type: Fuel type of car.
    - Transmission: Transmission type of car.
    - Insurance: Insurance information of the car.
    - Car Condition: Current car condition. A rating out of 5.

-  model_data.csv
   It contains information about the model and the current price of the model. This tells you the demand of the car today and whether it is still sold in market.
    - Model: Model name of the car that is sold.
    - Current Price: Current price of the car.
    
- train.py
  This python file contains a TrainModel class used to train the model. 
   
