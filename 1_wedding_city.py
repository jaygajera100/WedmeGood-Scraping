from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
import requests
from my_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    get_soup_data,
    BASE_URLS,
    CITY_NAMES,
)


class GenerateReport:
    def __init__(self, data, city):
        self.data = data
        self.city = city
        fieldnames = ['Photography', 'Rating',
                      'Location', 'Reviews', 'Price Per Day', 'Usefull', 'per day']
        with open(f"specific_city\{self.city}.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(self.data)


class GoogleMap_API:
    def __init__(self, base_urls, city_names):
        self.base_urls = base_urls
        self.city_names = city_names
        options = get_web_driver_options()
        set_browser_as_incognito(options)
        # set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        self.driver = get_chrome_web_driver(options)

    def run(self):
        print("Start Scripting...")
        self.driver.maximize_window()

        # According City Wise Urls
        j = 0
        for url in self.base_urls:
            fieldnames = ['Photography', 'Rating',
                          'Location', 'Reviews', 'Price Per Day', 'Usefull', 'per day']
            with open(f"specific_city\{self.city_names[j]}.csv", "w") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            try:
                self.driver.get(url)
                time.sleep(3)
                # Checking 404 Error
                try:
                    self.driver.find_element_by_xpath(
                        "//p[contains(@class, 'sc-esjQYD') and contains(@class, 'kqmPsf')]")
                    print(f'This {url} is not valid have wrong city')
                except Exception as e:
                    try:
                        pagenumbers = self.driver.find_element_by_xpath(
                            "//div[contains(@class, 'vendor-pagination') and contains(@class, 'center')]").text
                        pagenumbers_list = list(pagenumbers)
                        if len(pagenumbers_list) >= 10:
                            last_2_element = pagenumbers_list[-2:]
                            last_page = int(''.join(last_2_element))
                        else:
                            last_page = int(pagenumbers_list[-1])

                    except Exception as e:
                        last_page = 1

                    print(f'Looking for {url} Result')
                    page_count = 1
                    for page in range(1, last_page + 1):
                        # Scrolling the page slowly so that page loaded fully 108
                        time.sleep(1.5)
                        # i = 1
                        # while True:
                        #     try:
                        #         idd = f"card{i*19}"
                        #         locate = self.driver.find_element_by_id(idd)
                        #         self.driver.execute_script(
                        #             "arguments[0].scrollIntoView();", locate)
                        #         time.sleep(1.5)
                        #         i = i + 1
                        #         if i == 3:
                        #             break
                        #     except:
                        #         pass

                        # if page == 1:
                        #     id_list = [f'card{x}' for x in range(200)]  # 200
                        # else:
                        id_list = [f'card{x}' for x in range(40)]
                        list_elements = []
                        for x in id_list:
                            try:
                                body = self.driver.find_element_by_class_name(
                                    "VendorList")
                                single_element = body.find_element_by_id(
                                    x).text
                                elements = single_element.split('\n')
                                if len(elements) == 8:
                                    data = {
                                        'Photography': elements[0],
                                        'Rating': elements[1],
                                        'Location': elements[2],
                                        'Reviews': elements[3],
                                        'Price Per Day': elements[4],
                                        'Usefull': elements[5],
                                        'per day': elements[6],
                                    }

                                elif len(elements) == 7:
                                    data = {
                                        'Photography': elements[0],
                                        'Rating': elements[1],
                                        'Location': elements[2],
                                        'Reviews': elements[3],
                                        'Price Per Day': elements[4],
                                        'Usefull': elements[5],
                                        'per day': elements[6],
                                    }
                                elif len(elements) == 6:
                                    data = {
                                        'Photography': elements[0],
                                        'Rating': elements[1],
                                        'Location': elements[2],
                                        'Reviews': elements[3],
                                        'Price Per Day': elements[4],
                                        'Usefull': elements[5],
                                        'per day': 'None',
                                    }
                                elif len(elements) == 5:
                                    data = {
                                        'Photography': elements[0],
                                        'Rating': elements[1],
                                        'Location': elements[2],
                                        'Reviews': elements[3],
                                        'Price Per Day': elements[4],
                                        'Usefull': 'None',
                                        'per day': 'None',
                                    }
                                elif len(elements) == 4:
                                    data = {
                                        'Photography': elements[0],
                                        'Rating': elements[1],
                                        'Location': elements[2],
                                        'Price Per Day': elements[3],
                                        'Reviews': 'None',
                                        'Usefull': 'None',
                                        'per day': 'None',
                                    }

                                else:
                                    data = {
                                        'Photography': elements[0],
                                        'Rating': elements[1],
                                        'Location': elements[2],
                                        'Reviews': 'None',
                                        'Price Per Day': "None",
                                        'Usefull': 'None',
                                        'per day': 'None',
                                    }

                                list_elements.append(elements)
                                GenerateReport(data, self.city_names[j])

                            except Exception as e:
                                pass
                        print(f"Page {page} is Done")

                        page_count = page_count + 1

                        try:
                            page_element = self.driver.find_element_by_css_selector(
                                f"a[aria-label='Page {page+1}']")
                            page_element.send_keys(Keys.ENTER)
                        except Exception as e:
                            break

            except Exception as e:
                print(f"This {url} is not matched")
            j = j + 1
    


if __name__ == "__main__":
    am = GoogleMap_API(BASE_URLS, CITY_NAMES)
    am.run()
