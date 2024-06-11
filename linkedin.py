from random import randint

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time

# LinkedIn credentials
username = 'abc@example.com'
password = 'abc'
title = "CTO"
page_start = 1
page_end = 10

# Initialize the WebDriver
driver = webdriver.Chrome()


# Function to log in to LinkedIn
def linkedin_login(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    email_field = driver.find_element(By.ID, 'username')
    email_field.send_keys(username)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    sign_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
    sign_in_button.click()
    time.sleep(15)


# Function to check if already connected
def is_already_connected(driver, name):
    try:
        driver.find_element(By.XPATH, f'//*[contains(@aria-label, "Invite {name} to connect")]')
        return False
    except:
        return True


# Function to like a post
def like_post(driver, name):
    try:
        like_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Like')]")
        aria_pressed = like_button.get_attribute('aria-pressed')
        if aria_pressed != 'true':
            like_button.click()
            print(f"{name}: Liked recent post")
            time.sleep(2)
    except:
        pass


# Function to search for given title
def search_for(driver, title, page_start, page_end):
    try:
        profile_urls = []
        for iterator in range(page_start, page_end):
            driver.get(f'https://www.linkedin.com/search/results/people/?keywords={title}&page={iterator}')
            time.sleep(5)

            profiles = driver.find_elements(By.XPATH, '//span[contains(@class, "entity-result__title-text")]//a')
            for profile in profiles:
                url = profile.get_attribute('href')
                if url not in profile_urls:
                    profile_urls.append(url)

        print(f"Found {len(profile_urls)} profiles")
        return profile_urls
    except Exception as e:
        print(f"Error getting profiles: {e}")


# Function to send a connection request
def send_connection_request(driver, name):
    try:
        connect_button = driver.find_element(By.XPATH, f'//*[contains(@aria-label, "Invite {name} to connect")]')
        # Filthy hack to press a hidden button
        driver.execute_script("arguments[0].click();", connect_button)
        time.sleep(2)

        send_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Send")]')
        send_button.click()
        time.sleep(2)

        print(f"{name}: Connection request successful")

    except NoSuchElementException as e:
        print(f"{name}: Lost connect button: {e}")
    except Exception as e:
        print(f"{name}: Error sending connection request: {e}")


# Main script
linkedin_login(driver, username, password)

# Search for given title and get their profile URLs
prospect_profiles = search_for(driver, title, page_start, page_end)

for idx, profile_url in enumerate(prospect_profiles):
    print(f"{idx} - Requesting url: {profile_url}")
    driver.get(profile_url)
    time.sleep(5)
    name = driver.find_element(By.XPATH, '//h1[contains(@class, "text-heading-xlarge")]').text
    print(f"Grabbed name: {name}")
    connected = is_already_connected(driver, name)

    # Visit recent activity
    driver.get(driver.current_url + "/recent-activity/all/")
    time.sleep(5)
    # Like first post
    like_post(driver, name)

    if not connected:
        print(f"{name}: Sending connection request")
        # Head back to profile
        driver.get(profile_url)
        time.sleep(5)
        # Send connection request
        send_connection_request(driver, name)
    else:
        print(f"{name}: Already connected")

    # Sleep a random time until the next one
    time.sleep(randint(10,100))

driver.quit()