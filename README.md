# Twitter/X Political Sentiment

This repository addresses two issues I was curious about.

Firstly, since the change from Twitter to X, the X APIs have become frustrating to use. Features to read tweets are bundeled into a paid subscription ($100+/month), with the free tier having extremely limited capabilities. The code in this repository lets people scrape tweets for free using Selenium. All you need to do is change the search query and you have a great framework to accomplish this.

Secondly, with election season around the corner at the time of writing this, I was wondering what the political sentiment of twitter users was. After testing multiple judges (using text.py) I determined GPT-4 was the best at determining political bias within tweets. So I used GPT-4 to analyze the 1000 tweets I scraped using Selenium. I got 64.20% bias for Democrats and 34.30% bias for Republicans.

You can run all of this code yourself too! In your .env file add your twitter username and password. Then, Download "chromedriver" from https://googlechromelabs.github.io/chrome-for-testing/#stable and place the path of the driver's exe file in your .env. Finally, add your Open AI key and model to .env and then simply run the analysis.py file in terminal. If properly setup, this will scrape twitter then analyze the tweets.
