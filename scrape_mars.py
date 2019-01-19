from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():
    browser = init_browser()
    news = {}

    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

    news["news_title"] = news_title
    news["news_p"] = news_p
    news["news_date"] = news_date

    
    browser.quit()
    return news

def scrape_weather():
    browser = init_browser()
    mars_weather = {}
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    ol = soup.find('ol',id='stream-items-id')
    weather_li = ol.find_all('li')
    latest_weather = weather_li[0]
    latest_weather_p = latest_weather.find('p')
    mars_weather = latest_weather_p.text.strip()
    mars_weather["weather"] = mars_weather

    browser.quit()

    return mars_weather

def scrape_image():
    browser = init_browser()
    
    mars_image = {}

    jpl_url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

    mars_image["image"] = featured_image_url


    browser.quit()

    return mars_image


def scrape_facts():
    #browser = init_browser()
    mars_fact = {}

    mars_facts_url = 'http://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)
    mars_df = mars_table[0]
    mars_df.columns = ['Mars Fact', 'Value']
    #table_html = mars_df.to_html(index = True, header = None)
    mars_fact["dataframe"] = mars_df

    return mars_fact















