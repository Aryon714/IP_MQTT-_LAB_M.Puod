from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service  # Add this import
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import time
import json
from selenium.webdriver.chrome.options import Options

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless") 

def init_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # This keeps browser open
    # chrome_options.add_argument("--headless")  # Remove or comment this line
    
    # Configure service
    service = Service(executable_path='chromedriver.exe')  # Use your actual path
    
    # Initialize driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Initialize the WebDriver with Service
service = Service('chromedriver.exe')  # Just the filename
driver = init_driver()

url = "http://www.imdb.com"

def join_content(jc):
    return ','.join(jc)

def iterate_actors(iter_actors):
    m = []
    for item in iter_actors:
        m.append(item['name'])
    return ','.join(m)
        
def prepare_content(json_content):
    d = {}
    d['image'] = json_content['image']
    d['name'] = json_content['name']
    d['url_content'] = url + json_content['url']
    d['genre'] = join_content(json_content['genre'])
    d['actors'] = iterate_actors(json_content['actor'])
    d['description'] = json_content['description']
    d['trailer'] = url + json_content['trailer']['embedUrl']
    return d
    
def imdb_searchbox(url, link):
    driver.get(url)
    searchbox = driver.find_element(By.ID, "suggestion-search")
    searchbox.send_keys(link)
    time.sleep(2)
    searchbox.send_keys(Keys.ARROW_DOWN) 
    searchbox.send_keys(Keys.ENTER)
    #ActionChains(driver).key_down(ARROW_DOWN).key_up(ARROW_DOWN).key_down(ENTER).key_up(ENTER)
    #time.sleep(5)
    #print(link)
    #time.sleep(2)
    #print("1111")
    #driver.find_element(By.ID, "react-autowhatever-navSuggestionSearch--item-0").click()
    json_content = json.loads(driver.find_element(By.CSS_SELECTOR, 'script[type="application/ld+json"]').get_attribute("innerText"))
    return prepare_content(json_content)

def imdb_search(link, keep_open=False):
    s = imdb_searchbox(url, link)
    driver.get_screenshot_as_file("capture.png")
    if not keep_open:
        driver.quit()  # Only close if keep_open is False
    return s