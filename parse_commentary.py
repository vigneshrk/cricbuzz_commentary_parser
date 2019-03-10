
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re, os

chrome_driver_path = "./resources/chromedriver/chromedriver_linux"
options = Options()
options.binary_location = "/home/vignesh/proj/dev/resources/chrome-linux/chrome"
driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)

def open_url(url):
    driver.get(url)
    sleep(1)

def close_driver():
    driver.close()
    driver.quit()

def scrap_data():
    teams = []
    inns_btns = {}
    for elem in driver.find_elements_by_class_name("cb-nav-pill-1"):
        if "Inns" in elem.text:
            key = elem.text.split(" ")[0]
            inns_btns[key] = elem
            teams.append(key)

    BALL_PATTERN = "([0-9]+.[1-9]\n)"
    scrapped_data = {}
    for team in teams:
        scrapped_data[team] = []
        inns_btns[team].click()
        sleep(1)
        for elem in driver.find_elements_by_css_selector("div[ng-repeat='comm in match.commentary[set_innings_id]']"):
            text_content = elem.text
            if re.match(BALL_PATTERN, text_content):
                #print(text_content)
                #print("---")
                scrapped_data[team].append(text_content)
    print(scrapped_data)




if __name__ == '__main__':
    url = "https://www.cricbuzz.com/live-cricket-full-commentary/21538/ind-vs-aus-2nd-t20i-australia-tour-of-india-2019"
    open_url(url)
    scrap_data()
    close_driver()
