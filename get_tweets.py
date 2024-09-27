from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

# Get the top how many tweets
TWEETS_EXTRACTED = 1000

chrome_driver_path = os.getenv('DRIVER_PATH')
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://twitter.com/login")

try:
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    username_field.send_keys(os.getenv('TWITTER_USERNAME'))
    username_field.send_keys(Keys.RETURN)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys(os.getenv('TWITTER_PASSWORD'))
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)

    search_query = "American politics"
    url = f"https://twitter.com/search?q={search_query}&src=typed_query&f=live"
    driver.get(url)

    time.sleep(5)

    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)

    page_source = driver.page_source

finally:
    driver.quit()


soup = BeautifulSoup(page_source, 'html.parser')
tweets = soup.find_all('article', {'role': 'article'})

outputs = []
for tweet in tweets[:TWEETS_EXTRACTED]:
    content = tweet.find('div', {'data-testid': 'tweetText'}).get_text() if tweet.find('div', {'data-testid': 'tweetText'}) else "No text found"
    outputs.append(content)
    # user = tweet.find('span', {'class': 'css-901oao css-16my406'}).get_text() if tweet.find('span', {'class': 'css-901oao css-16my406'}) else "No user found"
    print(f"Content: {content}\n")

with open("output.txt", "w") as file:
    for item in outputs:
        file.write(item + "\n")
