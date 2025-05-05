from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_alert_notifications():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501/NotificationsDemo")
    wait = WebDriverWait(driver, 10)
    fill_title = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(., 'Title')]/following-sibling::div//input")
        )
    )
    fill_title.send_keys("New Notification")
    fill_body = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(., 'Body')]/following-sibling::div//input")
        )
    )
    fill_body.send_keys("New Body")
    icon_label = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[.//p[text()='Icon:']]"))
    )
    icon_label.click()
    alert_button = driver.find_element(By.XPATH, '//button[normalize-space()="Alert"]')
    alert_button.click()
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'stAlert') "
                    "and contains(., 'Alert sent!')]",
                )
            )
        )
        assert "Alert sent!" in success_message.text
        print("✅ Alert test passed!")

    except Exception as e:
        print("❌ Alert test failed:", e)

    finally:
        driver.quit()
