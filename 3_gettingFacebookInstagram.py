from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
import pandas as pd
import requests
from my_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    BASE_URLS,
)


class GoogleMap_API:
    def __init__(self, base_urls):
        self.base_urls = base_urls
        options = get_web_driver_options()
        set_browser_as_incognito(options)
        # set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        self.driver = get_chrome_web_driver(options)

    def run(self):
        print("Start Scripting...")
        self.driver.maximize_window()

        with open('city.txt') as f:
            cities = f.readlines()
            cities = [x.strip() for x in cities]
            for y in cities:
                try:
                    file_name = f'new\\{y}.csv'
                    df = pd.read_csv(file_name)
                    photographers = list(df['Photography'])
                    facebook_link = []
                    instagram_link = []
                    for x in photographers:
                        Check1, Check2 = False, False
                        pg_name = f"https://www.google.co.in/search?q={x}"
                        self.driver.get(pg_name)
                        time.sleep(1)
                        print(f"{x} Start")
                        try:
                            z = 1
                            zz = 1
                            result = self.driver.find_elements_by_class_name(
                                'g')
                            for i in result:
                                try:
                                    temp = i.find_element_by_class_name(
                                        'yuRUbf')
                                    link = temp.find_element_by_tag_name(
                                        'a').get_attribute('href')
                                    if z == 1:
                                        if 'facebook' in link:
                                            facebook_link.append(link)
                                            Check1 = True
                                            # print(link)
                                            z = z + 1
                                    if zz == 1:
                                        if 'instagram' in link:
                                            instagram_link.append(link)
                                            Check2 = True
                                            # print(link)
                                            zz = zz + 1
                                except:
                                    pass
                        except:
                            print("Didn't find search")
                        if Check1 == False:
                            facebook_link.append("None")
                        if Check2 == False:
                            instagram_link.append("None")

                except Exception as e:
                    # print(e)
                    # print(f"This {x} didn't find")
                    pass
                df['Facebook Link'] = pd.Series(facebook_link)
                df['Instagram Link'] = pd.Series(instagram_link)
                df.to_csv(f"All_new\\{y}.csv", index=False)
                print("Done")


if __name__ == "__main__":
    am = GoogleMap_API(BASE_URLS)
    am.run()
