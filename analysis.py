'''
This file can be used to analyze a set amount of recent tweets to determine their political bias.
To achieve this setup your .env with your twitter username and password. Also enter your OpenAI key and model.
Make sure you download the proper "chromedriver.exe" from https://googlechromelabs.github.io/chrome-for-testing/#stable.
Place the path of this driver in your .env file. Then simply run "python analysis.py" in the terminal; the code will run and print out results.
'''

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
# Max times you want to scroll to expand tweets
SCROLL_COUNT = 50

chrome_driver_path = os.getenv('DRIVER_PATH')
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://twitter.com/login")

tweets = []

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

    scroll_cur = 0
    previous_height = 0

    while len(tweets) < TWEETS_EXTRACTED:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        new_tweets = soup.find_all('article', {'role': 'article'})

        for tweet in new_tweets:
            content = tweet.find('div', {'data-testid': 'tweetText'}).get_text() if tweet.find('div', {'data-testid': 'tweetText'}) else "No text found"
            if content not in tweets:
                tweets.append(content)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            print("No more tweets to load.")
            break
        previous_height = new_height

        scroll_cur += 1
        if scroll_cur >= SCROLL_COUNT:
            break

finally:
    driver.quit()


democrat_count = 0
republican_count = 0
total_tweet_count = 0
model = os.getenv("MODEL_NAME")
custom_prompt = "Is this following tweet more favorable for the Republican or Democratic party. Reply with either 'Democratic' or 'Republican'. Do NOT say anything else besides that one word. \n "

def get_chatgpt_response(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

for line in tweets[:TWEETS_EXTRACTED]:
    total_tweet_count += 1
    line = line.strip()
    if line:
        response = get_chatgpt_response(custom_prompt + line)
        if "Democrat" in response:
            democrat_count += 1
        elif "Republican" in response:
            republican_count += 1

# Use this to write everything into a text file to analyze if needed

# with open("output.txt", "w") as file:
#     for item in tweets:
#         file.write(item + "\n")

print(f"Of the {total_tweet_count} tweets scraped, {democrat_count} ({round(democrat_count/total_tweet_count, 4)*100}%) tweets had a bias for the Democratic party and {republican_count} ({round(republican_count/total_tweet_count, 4)*100}%) tweets had a bias for the Republican party, when using {model} as a judge")