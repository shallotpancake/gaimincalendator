from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json 
import time
import platform
import zipfile
import os
import env_setup

# helpers

def find_file_in_tree(start_dir, target_filename):
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(start_dir):
        # Check if the target file is in the current directory
        if target_filename in filenames:
            # If found, return the full path of the file
            return os.path.join(dirpath, target_filename)
    return None  # If file is not found

def get_platform():
    platforms = {
    'Windows': 'win64',
    'Darwin': 'mac-arm64',
    'Linux': 'linux64'
    }
    
    return platforms[platform.system()] or None

def get_download_url():
    platform = get_platform()
    endpoint = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
    response = requests.get(endpoint)
    downloads = (json.loads(response.text))['channels']['Stable']['downloads']
    url = next((item['url'] for item in downloads['chromedriver'] if item['platform'] == platform), None)
    
    return url

# do-ers

def download_chromedriver():
    url = get_download_url()
    # download driver archive
    requests.get(url, stream=True)
    response = requests.get(url, stream=True)
    
    os.makedirs(os.environ.get('TEMPFILE_DIRECTORY'), exist_ok=True)
    chromedriver_archive = os.path.abspath(os.path.join(os.environ.get('TEMPFILE_DIRECTORY'), 'chromedriver.zip'))
    
    with open(chromedriver_archive, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print(f"File downloaded and saved as {chromedriver_archive}")
    
    # unpack driver archive
    os.makedirs(os.environ.get('DRIVER_DIRECTORY'), exist_ok=True)
    chromedriver_file = os.path.abspath(os.path.join(os.environ.get('DRIVER_DIRECTORY'), 'chromedriver.exe'))

    with zipfile.ZipFile(chromedriver_archive, 'r') as zip_ref:
        zip_ref.extractall(chromedriver_file)

    print(f"Files have been extracted to {chromedriver_file}")


    
def get_tier_1_source(url):    

    driver_path = find_file_in_tree(os.path.join(os.getcwd(), os.environ.get('DRIVER_DIRECTORY')), os.environ.get('DRIVER_EXE'))
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url) 
    time.sleep(5)
    
    try:
        # Assuming the close button has a unique class or ID
        close_button = driver.find_element(By.CSS_SELECTOR, ".app-popup button")  # Use appropriate selector (e.g., class, ID, etc.)
        ActionChains(driver).move_to_element(close_button).click(close_button).perform()
        print("Overlay closed.")
    except Exception as e:
        print(f"No overlay found or unable to close: {e}")
    
    # toggle all on
    all_button = driver.find_element(By.CSS_SELECTOR, "span[data-filter-on='all']")
    ActionChains(driver).move_to_element(all_button).click(all_button).perform()
    
    # toggle all off
    all_button = driver.find_element(By.CSS_SELECTOR, "span[data-filter-on='all']")
    # The line `ActionChains(driver).move_to_element(all_button).click(all_button).perform()` is using
    # the `ActionChains` class from Selenium to perform a series of actions on a web element. Here's a
    # breakdown of what each part of the line is doing:
    ActionChains(driver).move_to_element(all_button).click(all_button).perform()
    
    time.sleep(3)
    
    # toggle tier 1 on
    tier1_button = driver.find_element(By.CSS_SELECTOR, "span[data-filter-on='1']")
    ActionChains(driver).move_to_element(tier1_button).click(tier1_button).perform()
    
    time.sleep(3)

    html = driver.page_source
    
    new_match_style_div = driver.find_element(By.CSS_SELECTOR, "div.new-match-style")
    matches_html = new_match_style_div.get_attribute('outerHTML')
        

    driver.quit()
    
    return matches_html

if __name__ == "__main__":
    download_chromedriver()
    print(get_tier_1_source("https://liquipedia.net/dota2/Liquipedia:Matches"))
    