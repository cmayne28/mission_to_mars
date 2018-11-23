from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd 

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #NASA Mars News 
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text

    #JPL Mars Space Images - Featured Image
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    img = soup.find(class_="carousel_item")["style"]
    img1 = img.split("'")
    img2 = img1[1]

    featured_image_url = "https://www.jpl.nasa.gov" + img2 

    # Mars Weather

    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('div', class_="js-tweet-text-container").text.strip()

    # Mars Facts

    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.

    tables = pd.read_html(url_facts)

    df = tables[0]

    df.columns = ['', 'Value']

    df1 = df.set_index("")

    mars_table = df.to_html()


    #Mars Hemispheres

    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup.prettify())

    hemisphere_names = []
    mars_hemis = []

    for x in range(4):
        hems = soup.find_all('h3')[x].text
        hemisphere_names.append(hems)

    for x in range(4):
        mars_hem_images = browser.find_by_tag('h3')
        mars_hem_images[x].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find("img", class_="wide-image")["src"]
        img_url = 'https://astrogeology.usgs.gov'+ image
        mars_hemis.append(img_url)
        browser.back()

    hemisphere_image_urls = [{"title": hemisphere_names[x], "img_url": mars_hemis[x]} for x in range(4)]

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls" : hemisphere_image_urls,
        "mars_table": mars_table}
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
