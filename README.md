# Car Price Prediction

### **About:**
The main aim of this project was to help the users willing to buy a used car to estimate the approximate selling price of the car they are buying to make sure they are priced appropriately and not overpaying. This project also helps users selling their car to get an idea of what would be an appropriate price for their vehicle and then sell their car accordingly. The application takes various inputs from the user like car condition, distance covered by the car, transmission type. It then predicts an approximate price that might be ideal depending on the car conditions provided. 

### Images of Application

Landing page
![landing page](https://github.com/AnkitS97/car-price-prediction/blob/main/image1.PNG?raw=true)


Prediciton page
![prediction page](https://github.com/AnkitS97/car-price-prediction/blob/main/image2.PNG?raw=true)

### Features

- scrapper.py\
  The scrapper.py file is used to scrapper data from various websites. Run the scrapper.py file to generate dataset by scrapping data from websites like [Car Dekho](https://www.cardekho.com/) and [Car Wale](https://www.carwale.com/).\
   It uses selenium to first extract urls of different vehicles available on used car selling websites and then it hits these urls iteratively to get the necessary inforamtion out    of it. At the end, it generates 2 csv files.

- car_data.csv\
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

-  model_data.csv\
   It contains information about the model and the current price of the model. This tells you the demand of the car today and whether it is still sold in market.
    - Model: Model name of the car that is sold.
    - Current Price: Current price of the car.\

Data used is in tabular format with 9 independent features across two CSV files and 1 target feature.
The features are a mixture of both numerical and categorical.
There is a total of 2532 rows of data.\
    
- train.py\
  This python file contains a TrainModel class used to train the model.\
  This file first does data preprocessing by combining the two datasets by doing a merge on a common column 'model'. It then continues processing by removing unnecessary columns, imputing null values using strategies like imputing using mean or median, scaling the data using StandardScaler, converting categorical features to numerical featrures using OneHotEncoder and LabelEncoder and generating new features using the available features.\
  
This application is easily trainable. Adding a '/train' to the URI would give you the URI to train the model and save it. It also generates logs for each user activity and also for exceptions thrown. It has a plug-and-play architecture and thus it is easily deployable on any web based api or cloud platform. This application contains files to deploy it on AWS.

### How to run

> Note: Once you clone the project make sure to replace the chrome driver with a chrome driver according to your version of chrome browser. You can download a chrome driver from [here](https://chromedriver.storage.googleapis.com/index.html). Chrome driver is used to scrape the data over internet.

- Open anaconda prompt

- Create a new enivironment
    `conda create -n <env name> python==3.8`
    
- Navigate within anaconda prompt to the directory where you have cloned this project

- To install all the dependencies
    `pip install -r requirements.txt`
    
- To run the app
    `python application.py`

This command will output a local url where it has hosted the application.

### Challenges

The major challenge faced during this project was scrapping data. There was no dataset available online with the features of car condition and current selling price. So I decided to scrape my own data. It was difficult to adapt to the different formats of various websites. I managed to do so using exception handling and adding checks to know the site. Then it was also difficult to clean the data. The data obtained was in a very raw format like the price would sometimes be in number like 750000 and sometimes it would be in a string like “Rs.7.50 Lakh”. It was challenging all such scenarios in various features.
   

