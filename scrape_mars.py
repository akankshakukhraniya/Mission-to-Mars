
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape():

    browser = Browser('chrome', **executable_path, headless=False)
    title, paragraph = news(browser)
    mars = {
        'title': title,
        'paragraph': paragraph,
        'image': get_image(browser),
        'facts': facts(),
        'hemispheres': hemi(browser)
    }
    return mars
    

# Visit Mars news URL page 
def news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_news_title = soup.find('li', class_='slide')
    news_title = mars_news_title.find('div', class_='content_title').text
    news_para = mars_news_title.find('div', class_="article_teaser_body").text
    return news_title, news_para

# ## Scraping JPL Featured Image URL
# visit the JPL Featured Space Image website
def get_image(browser):
    jpl_img_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_img_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    return browser.find_by_css('img.fancybox-image')['src']

# Visit the Mars Facts webpage
def facts():
    facts_webpg = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_webpg)
    facts_df = table[0]
    facts_df.columns = ['Description', 'Value']
    facts_df['Description'] = facts_df['Description'].str.replace(':','')
    return facts_df.to_html()

# Visit the USGS Astrogeology site 
def hemi(browser):
    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_url)
    links = browser.find_by_css('a.itemLink h3')
    hemispheres = []
    for i in range(len(links)):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[0].click()
        hemisphere['url'] = browser.find_link_by_partial_text('Sample')['href']
        hemispheres.append(hemisphere)    
        browser.back()
    browser.quit()
    return hemispheres
