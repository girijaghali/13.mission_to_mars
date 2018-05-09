# Dependencies
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape() :

    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    #!which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    ### NASA Mars News
    # URL of page to be scraped
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html_news = browser.html
    soup = BeautifulSoup(html_news, 'html.parser')
    headlines = soup.find_all('div', class_="list_text")
    news_title = headlines[0].find('div', class_="content_title").text
    news_p = headlines[0].find('div', class_="article_teaser_body").text

    ### JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')
    featured_images = soup.find_all('div', class_="carousel_items")
    img_url = featured_images[0].find('a')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov'+ img_url


    ### Mars Weather
    # URL of page to be scraped
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')
    weather_tweet = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = weather_tweet[0].text

    ### Mars Facts
    # URL of page to be scraped
    url_facts = 'http://space-facts.com/mars/'
    facts_table = pd.read_html(url_facts)
    facts_df = facts_table[0]
    facts_df.columns = ["",""]
    #facts_df = facts_df.set_index('Key')
    html_table = facts_df.to_html(index = False)
    #html_table.replace('\n', '')

    ### Mars Hemisperes
    # URL of page to be scraped
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    image_short_link = []
    image_link = []
    image_title = []
    image_main_link = []
    all_images = soup.find_all('div',class_='item')
    #print(all_images)
    for image in all_images:
        shrt_link = image.find('a',class_="itemLink product-item")['href']
        link = 'https://astrogeology.usgs.gov'+shrt_link
        title = image.find('h3').text
    
        image_short_link.append(shrt_link)
        image_link.append(link)
        image_title.append(title)
    
        browser.click_link_by_partial_text(title)
        html_hemisphere_img = browser.html
        soup = BeautifulSoup(html_hemisphere_img, 'html.parser')
        big_link = soup.find('div',class_='downloads').a['href']
        image_main_link.append(big_link)
        browser.click_link_by_partial_text('Back')
    hemisphere_image_urls =[]
    i=0
    while i<len(image_main_link):
        hemisphere_image_urls.append({
                                    'title':image_title[i]
                                  , 'img_url':image_main_link[i]
                                })
        i=i+1

    all_scraped_mars_data = {}

    all_scraped_mars_data['NewsTitle'] = news_title
    all_scraped_mars_data['NewsP'] = news_p
    all_scraped_mars_data['FeaturesImage'] = featured_image_url
    all_scraped_mars_data['MarsWeather'] = mars_weather
    all_scraped_mars_data['Mars_Facts'] = html_table
    all_scraped_mars_data['Hemisphere'] = hemisphere_image_urls

    return  all_scraped_mars_data
