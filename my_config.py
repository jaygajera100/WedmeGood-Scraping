from selenium import webdriver
import requests

# According to City wise
with open('city.txt') as f:
    city_names = f.readlines()
CITY_NAMES = [x.strip() for x in city_names]

BASE_URLS = [
    f'https://www.wedmegood.com/vendors/{x}/wedding-photographers/' for x in city_names]



def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver", chrome_options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')
