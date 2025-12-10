import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://example.com/login")
    yield driver
    driver.quit()

def test_login_with_invalid_password(setup):
    driver = setup
    try:
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys("valid_user@example.com")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("InvalidPassword")

        login_button = driver.find_element(By.ID, "loginButton")
        login_button.click()

        error_message = driver.find_element(By.ID, "errorMessage")
        assert "Invalid username or password" in error_message.text, "Error message not displayed."

    except Exception as e:
        pytest.fail(f"Test failed due to exception: {e}")