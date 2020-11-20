from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
import selenium
import pymongo

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.March_tweets
collection = db.trends
collection2 = db.tweets

path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://us.trend-calendar.com/trend/2020-03-01.html")
time.sleep(2)
# Gets Trends from trend calendar webpage
March = []
March_dict = {}
for date in trend_dates:
    trend_dict = {}
    for trend in trend_dates[date]:
        driver.get(trend['URL'])
        time.sleep(1.5)
        counter = 3
        text_tweets = []
        while counter != 0:
            try:
                time.sleep(2)
                contents = driver.find_element_by_class_name("css-1dbjc4n")
                contents_html = contents.get_attribute("innerHTML")
                soup = bs(contents_html)
                tweet_html = soup.find_all("div", {"data-testid":"tweet"})
                for tweet in tweet_html:
                    text = tweet.find("div", class_ = "css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").get_text()
                    text_tweets.append(text)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                counter -= 1
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                counter -= 1
            trend_dict[trend['trends']] = text_tweets
        March.append(text_tweets)
        time.sleep(1)
    March_dict[date]={"Tweet":trend_dict}

collection2.insert_one(March_dict)
#Login into Twitter
driver.get("https://www.twitter.com/login")
time.sleep(1)
usernameInput = driver.find_element_by_name("session[username_or_email]")
passwordInput = driver.find_element_by_name("session[password]")
usernameInput.send_keys("chuck45630256")
passwordInput.send_keys("Longbow1@")
passwordInput.send_keys(Keys.ENTER)
time.sleep(5)

March = []
March_dict = {}
trend_dict = {}
for date in trend_dates:
    for trend in trend_dates[date]:
        driver.get(trend['URL'])
        time.sleep(1.5)
        counter = 3
        text_tweets = []
        while counter != 0:
            try:
                time.sleep(2)
                contents = driver.find_element_by_class_name("css-1dbjc4n")
                contents_html = contents.get_attribute("innerHTML")
                soup = bs(contents_html)
                tweet_html = soup.find_all("div", {"data-testid":"tweet"})
                for tweet in tweet_html:
                    text = tweet.find("div", class_ = "css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").get_text()
                    text_tweets.append(text)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                counter -= 1
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                counter -= 1
            trend_dict[trend['trends']] = text_tweets
        March_dict[date]={"Tweet":trend_dict}
        March.append(text_tweets)
        time.sleep(1)

collection2.insert_one(March_dict)
#Save tweets into a file
chunks = [March[x:x+3] for x in range(0, len(March), 3)]

with open('March tweets separated by day text.csv', 'w', encoding="utf-8") as filehandle:
    for listitem in chunks:
        filehandle.write('%s\n' % listitem)