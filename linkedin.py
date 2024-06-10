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
def is_already_connected(driver):
    try:
        driver.find_element(By.XPATH, '//*[contains(@aria-label, "Invite")]')
        return False
    except:
        return True

# Function to like a post
def like_post(driver):
    try:
        like_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Like')]")
        aria_pressed = like_button.get_attribute('aria-pressed')
        if aria_pressed != 'true':
            like_button.click()
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
def send_connection_request(driver):
    try:
        connect_button = driver.find_element(By.XPATH, '//*[contains(@aria-label, "Invite")]')
        # Filthy hack to press a hidden button
        driver.execute_script("arguments[0].click();", connect_button)
        time.sleep(2)

        send_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Send")]')
        send_button.click()
        time.sleep(2)

        print(f"Connection request successful")

    except NoSuchElementException as e:
        print(f"No connect button - already connected")
    except Exception as e:
        print(f"Error sending connection request: {e}")


# Main script
linkedin_login(driver, username, password)

# Search for given title and get their profile URLs
prospect_profiles = search_for(driver, title, page_start, page_end)

for idx, profile_url in enumerate(prospect_profiles):
    print(f"{idx} - Requesting url: {profile_url}")
    driver.get(profile_url)
    time.sleep(5)
    connected = is_already_connected(driver)

    # Visit recent activity
    driver.get(driver.current_url + "/recent-activity/all/")
    time.sleep(5)
    # Like first post
    like_post(driver)

    if not connected:
        # Head back to profile
        driver.get(profile_url)
        time.sleep(5)
        # Send connection request
        send_connection_request(driver)
    else:
        print(f"Already connected to {profile_url}")

    # Sleep a random time until the next one
    time.sleep(randint(10,100))

driver.quit()