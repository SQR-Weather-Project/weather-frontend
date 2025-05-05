from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_push_notifications(driver):
    driver.get("http://localhost:8501/NotificationsDemo")

    wait = WebDriverWait(driver, 10)

    fill_title = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//label[contains(., 'Title')]/following-sibling::div//input")
        )
    )
    fill_title.send_keys("New Notification")

    fill_body = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//label[contains(., 'Body')]/following-sibling::div//input")
        )
    )
    fill_body.send_keys("New Body")

    icon_label = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[.//p[text()='Icon:']]"))
    )
    icon_label.click()

    push_button = driver.find_element(By.XPATH,
                                      '//button[normalize-space()="Push"]')
    push_button.click()

    try:
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'stAlert') "
                    "and contains(., 'Push notification sent!')]",
                )
            )
        )
        assert "Push notification sent!" in success_message.text
        print("✅ Push Notification test passed!")
    except Exception as e:
        print("❌ Push Notification test failed:", e)
        raise
