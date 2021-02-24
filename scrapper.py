from selenium import webdriver
import time
import pandas as pd


def get_cars_data(web_driver_path: str):
    with webdriver.Chrome(executable_path=web_driver_path) as wd:
        res = scrape_car_data(wd)

    df = pd.DataFrame(data=res)
    df.to_csv('car_data.csv')


def scrape_car_data(wd: webdriver):
    def scroll_to_end(wd: webdriver):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    search_url = "https://www.cars24.com/buy-used-cars-new-delhi/?itm_source=Cars24Website&itm_medium=sticky_header"

    wd.get(search_url)

    all_cars = []
    cars_count = 0
    cars_models = set()
    result_start = 0
    number_of_thumbnails = 0
    car_urls = set()

    while number_of_thumbnails < 5000:
        scroll_to_end(wd)
        time.sleep(1)
        thumbnails = wd.find_elements_by_css_selector("div.col-4 a._20d39")
        if len(thumbnails) == number_of_thumbnails:
            break
        print(f"looping through {number_of_thumbnails}.")
        number_of_thumbnails = len(thumbnails)

    car_urls = {thumb.get_attribute('href') for thumb in thumbnails if thumb.get_attribute('href')}
    # for i in range(5000):
    #     thumb = thumbnails[i]
    #     if thumb.get_attribute('href'):
    #         car_urls.add(thumb.get_attribute('href'))

    for url in car_urls:
        wd.get(url)
        time.sleep(1)
        # try:
        #     time.sleep(1)
        #     thumbnails[cars_count].click()
        #     time.sleep(1)
        # except Exception as e:
        #     try:
        #         wd.back()
        #     except Exception as exp:
        #         print("go back exception")
        #         continue
        #     continue

        model, car = get_car_details(wd)
        if car is not None:
            cars_models.add(model)
            all_cars.append(car)

        cars_count = len(all_cars)
        if cars_count >= 5000:
            print(f"Found: {cars_count} Cars data.")
            break
        # try:
        #     wd.back()
        # except Exception as e:
        #     print("go back exception")
        #     continue

        # result_start = number_of_thumbnails
        # wd.back()
    # model, car = get_car_details(wd)
    # cars_models.add(model)
    # df = pd.DataFrame(cars_models)
    # df.to_csv('models.csv')
    # all_cars.append(car)
    # wd.back()

    df = pd.DataFrame(cars_models)
    df.to_csv('models.csv')
    print(f"Found: {len(cars_models)} models.")
    return all_cars


def get_car_details(wd: webdriver):
    cars_models = set()
    car = []
    model = wd.find_elements_by_css_selector("p._342La")
    if len(model) == 0:
        model = wd.find_elements_by_css_selector("p._3Uk5w")
    if len(model) == 0:
        return None, None
    model = ''.join(model[0].text.split(' ')[1:-1])
    cars_models.add(model)
    car.append(model)
    try:
        price = int(wd.find_element_by_css_selector("h4._3NnL0").text.split(' ')[1].replace(',', ''))
    except Exception as e:
        price = int(wd.find_element_by_css_selector("h4._3AzX6").text.split(' ')[1].replace(',', ''))
    car.append(price)
    car_info = wd.find_elements_by_css_selector("._3fGRT p")
    km_driven = int(car_info[0].text.split(' ')[0].replace(',', ''))
    year = int(car_info[1].text.split(' ')[1])
    owner = car_info[2].text
    fuel = car_info[3].text
    transmission = car_info[4].text
    if len(car_info) >= 7:
        insurance = car_info[6].text
    else:
        insurance = None
    car.append(km_driven)
    car.append(year)
    car.append(owner)
    car.append(fuel)
    car.append(transmission)
    car.append(insurance)
    condition = float(wd.find_element_by_css_selector("._3QE6A p").text.split('\n')[0])
    car.append(condition)
    return model, car


def get_model_price(web_driver_path):
    model_df = pd.read_csv('models.csv')
    models = model_df['0'].values

    with webdriver.Chrome(executable_path=web_driver_path) as wd:
        res = get_price(wd, models)

    price_df = pd.DataFrame(res)
    mod = pd.concat([model_df, price_df], axis=1)
    # mod.columns = ['0', '1']
    mod.to_csv('new_models.csv')


def get_price(wd: webdriver, models):
    model_prices_df = pd.read_csv('new_models.csv')
    model_prices = model_prices_df['0.1'].values
    prices = list(model_prices)
    # prices = [0] * len(models)
    for i, model in enumerate(models):
        print(i)
        if prices[i] != '0':
            continue
        search_url = "https://www.google.com/search?q=new+{q}+car+price&rlz=1C1RXQR_enIN932IN932&oq=new+{q}+car+price&aqs=chrome..69i57.755j0j7&sourceid=chrome&ie=UTF-8"
        wd.get(search_url.format(q=model))
        time.sleep(1)
        try:
            urls = wd.find_elements_by_css_selector(".g .tF2Cxc .yuRUbf a")
        except Exception as e:
            continue
        for url in urls:
            if url.get_attribute('href') and ("carwale" in url.get_attribute('href') or "cardekho" in url.get_attribute('href')):
                car_url = urls[1].get_attribute('href')
                wd.get(car_url)
                time.sleep(1)
                try:
                    if "carwale" in car_url:
                        price = wd.find_element_by_css_selector("span.o-eqqVmt").text
                    else:
                        price = wd.find_element_by_css_selector("div.price").text
                    time.sleep(1)
                    print(f"Found price {price}")
                    if price == '|':
                        price = input("Enter price ")
                        price = "Rs." + price + " Lakh"
                    prices[i] = price
                    break
                except Exception as e:
                    price = input("Enter price ")
                    prices[i] = "Rs." + price + " Lakh"
                    break

    return prices


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver_path = "chromedriver.exe"
    get_cars_data(driver_path)

    get_model_price(driver_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
