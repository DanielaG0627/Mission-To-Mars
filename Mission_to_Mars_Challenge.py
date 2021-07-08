#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[11]:


#set up executable path and URL for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[17]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[10]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[11]:


slide_elem.find('div', class_='content_title')


# In[12]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[13]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[18]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[23]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[24]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[25]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[26]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[30]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[31]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[12]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[14]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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


# In[15]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[16]:


# 5. Quit the browser
browser.quit()


# In[ ]:




