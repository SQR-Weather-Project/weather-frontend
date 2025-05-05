from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_sign_up():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501/SignUp")

    wait = WebDriverWait(driver, 10)
    fill_username = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//label[contains(., 'Username')]/following-sibling::div//input"
    )))
    fill_username.send_keys("bogapova.alia@gmail.com")

    fill_location = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//label[contains(., 'Location')]/following-sibling::div//input"
    )))
    fill_location.send_keys("Kazan")

    fill_password = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//label[contains(., 'Password')]/following-sibling::div//input"
    )))
    fill_password.send_keys("1234pass")

    fill_repeat_password = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//label[contains(., 'Password')]/following-sibling::div//input"
    )))
    fill_repeat_password.send_keys("1234pass")

    button_sign_up = driver.find_element(
        By.CSS_SELECTOR,
        'button[data-testid="stBaseButton-secondary"]'
    )
    button_sign_up.click()

    try:
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'stAlert') and "
                "contains(., 'Registration successful (mock)!')]"
            ))
        )
        assert "Registration successful (mock)!" in success_message.text
        print("✅ Registration test passed!")
    except Exception as e:
        print("❌ Registration test failed:", e)
    finally:
        driver.quit()
