# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get('https://www.amazon.com')

try:
    # Search for mobiles
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys('mobiles')
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(3)

    # Add first three mobiles to the cart
    for i in range(3):
        mobiles = driver.find_elements(By.CSS_SELECTOR, '.s-main-slot .s-result-item')
        if i < len(mobiles):
            mobile = mobiles[i]
            try:
                add_to_cart_button = mobile.find_element(By.CSS_SELECTOR, 'input[name="submit.add-to-cart"]')
                add_to_cart_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Could not add mobile {i+1} to the cart: {e}")
        else:
            print(f"Less than {i+1} mobiles found on the page.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
