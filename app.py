from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#HTML page route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#Scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   #upsert = true create a new document if one doesn't already exist, and new data will always be saved
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

#run the app
if __name__ == "__main__":
   app.run()

#Article title and summary
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


#Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

#Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

#Hemisphere Images
def scrape_hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    #retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        #create an empty dictionary
        hemispheres = {}
        #click on each hemisphere link
        hemisphere_link = browser.find_by_tag('h3')[i].click()
        #parse the resulting html
        html = browser.html
        img_soup = soup(html, 'html.parser')
        #retrieve the image title
        title = img_soup.find('h2', class_='title').get_text()
        #retreive the image url string and title for the hemisphere image
        img_url_rel = img_url_rel = img_soup.find('img', class_='wide-image').get('src')
        img_url = f'https://marshemispheres.com/{img_url_rel}'
        #save image url string as the value for the img_url key
        for pair in ["img_url", "title"]:
            hemispheres[pair] = eval(pair)
        #add the dictionary to the list
        dictionary_copy = hemispheres.copy()
        if dictionary_copy not in hemisphere_image_urls:
            hemisphere_image_urls.append(dictionary_copy)
        #browser back
        browser.back()
    return None