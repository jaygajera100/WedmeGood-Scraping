from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
import requests
import pandas as pd
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

        self.driver.get('https://www.facebook.com/')
        time.sleep(3)
        email = self.driver.find_element_by_id('email')
        email.send_keys('##########')  # Enter Email id of facebook

        password = self.driver.find_element_by_id('pass')
        password.send_keys('#######')  # Enter password of Facebook
        time.sleep(1)

        submit = self.driver.find_element_by_name('login')
        submit.send_keys(Keys.ENTER)
        time.sleep(3)

        with open('specific_city.txt') as f:
            cities = f.readlines()
            cities = [x.strip() for x in cities]
            for y in cities:
                file_name = f'All_new\\{y}.csv'
                df = pd.read_csv(file_name)
                facebook = df['Facebook Link']
                count = 0
                for x in facebook:
                    check_email = False
                    check_website = False
                    check_contact = False
                    print(x)
                    try:
                        self.driver.get(x)
                        time.sleep(2)
                        body = self.driver.find_elements_by_xpath(
                            "//div[contains(@class, 'sjgh65i0') and contains(@class, 'cbu4d94t') and contains(@class, 'j83agx80')]")

                        for b in body[:2]:
                            time.sleep(1)
                            if check_email or check_contact or check_website:
                                break
                            else:
                                content = b.text
                                content_list = content.split('\n')
                                z, zz, zzz = 1, 1, 1
                                for x in content_list:
                                    # For Email Id:
                                    if z == 1:
                                        if '@' in x:
                                            email = x
                                            check_email = True
                                            z = z + 1
                                    # For Website Link
                                    if zz == 1:
                                        if ('www' in x.lower()) or ('.co.in' in x.lower()) or ('.in' in x.lower()) or ('.com' in x.lower()) or ('http:' in x.lower()):
                                            if '@' in x:
                                                pass
                                            else:
                                                website = x
                                                check_website = True
                                                zz = zz + 1
                                    # For Contact Only
                                    if zzz == 1:
                                        # If contact like = +919825753290 or +1547524889
                                        if ("+91" in x) or ("+1" in x):
                                            contact = x
                                            check_contact = True
                                            zzz = zzz + 1
                                        else:
                                            try:
                                                xx = x.split(' ')
                                                if len(xx) == 2:
                                                    xxx = ''.join(xx)
                                                    yy = int(xxx)
                                                    # If contact like = 98257 53290
                                                    if yy >= 1000000:
                                                        contact = yy
                                                        check_contact = True
                                                        zzz = zzz + 1

                                                elif len(xx) == 1:
                                                    yy = int(x)
                                                    # If contact like = 9825753290
                                                    if yy >= 1000000:
                                                        contact = yy
                                                        check_contact = True
                                                        zzz = zzz + 1
                                                else:
                                                    pass
                                            except:
                                                pass
                    except:
                        pass
                    if check_email == False:
                        email = "None"
                    if check_website == False:
                        website = "None"
                    if check_contact == False:
                        contact = "None"

                    df.iloc[count, 8] = contact  # 8
                    df.iloc[count, 7] = email  # 7
                    df.iloc[count, 11] = website  # 11
                    df.to_csv(f"All_done\\{y}.csv", index=False)
                    count = count + 1
            print('Done')


if __name__ == "__main__":
    am = GoogleMap_API(BASE_URLS)
    am.run()
