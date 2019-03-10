
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re, os
import configparser


chrome_driver_path = "./resources/chromedriver/chromedriver_linux"
options = Options()
config = configparser.ConfigParser()
if 'chrome_binary_location' in config['DEFAULT']:
    options.binary_location = config['DEFAULT']['chrome_binary_location']
    print('using custom chrome from '+options.binary_location)
else:
    print('using default chrome')
driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)

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

    BALL_PATTERN = "([0-9]+\.[1-9]+\\n.+?, )"
    scrapped_data = {}
    for team in teams:
        scrapped_data[team] = []
        inns_btns[team].click()
        sleep(1)
        for elem in driver.find_elements_by_css_selector("div[ng-repeat='comm in match.commentary[set_innings_id]']"):
            text_content = elem.text
            m = re.match(BALL_PATTERN, text_content)
            if m:
                ball_data = {}
                ball_info = m.groups()[0]
                # ball_event = text_content.lstrip(ball_info)
                ball_event = text_content.replace(ball_info, "")
                result = ball_event.split(",")[0]
                story = ball_event.replace(result+", ", "")
                ball_info = ball_info.rstrip(", ")
                ball_info = ball_info.split("\n")
                ball_num = ball_info[0]
                players = ball_info[1].split(" to ")
                ball_data["ball_num"] = ball_num
                ball_data["bowler"] = players[0]
                ball_data["batsman"] = players[1]
                ball_data["result"] = result
                ball_data["story"] = story
                scrapped_data[team].append(ball_data)


    print(scrapped_data)



if __name__ == '__main__':
    url = "https://www.cricbuzz.com/live-cricket-full-commentary/21538/ind-vs-aus-2nd-t20i-australia-tour-of-india-2019"
    open_url(url)
    scrap_data()
    close_driver()
