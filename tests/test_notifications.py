import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_notification_settings():
    driver = webdriver.Chrome(service=Service())
    driver.get("http://localhost:8501/Notifications")

    wait = WebDriverWait(driver, 15)

    slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stSlider")))
    move_slider_to_value(driver, slider, 30)

    param_select = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//label[contains(., 'choose a parameter')]/following-sibling::div",
            )
        )
    )
    param_select.click()
    option_temp = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Temperature']"))
    )
    option_temp.click()

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[contains(., 'choose a filter')]/following-sibling::div")
        )
    )

    filter_select = driver.find_element(
        By.XPATH, "//label[contains(., 'choose a filter')]/following-sibling::div"
    )
    filter_select.click()
    option_above = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='above']"))
    )
    option_above.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))

    number_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='number']"))
    )
    number_input.send_keys(Keys.CONTROL + "a")
    number_input.send_keys(Keys.BACKSPACE)
    number_input.send_keys("20")

    city_select = driver.find_elements(
        By.XPATH, "//label[contains(., 'Select a city')]/following-sibling::div"
    )[-1]
    city_select.click()
    option_kazan = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Kazan']"))
    )
    option_kazan.click()

    driver.execute_script("document.body.click();")
    time.sleep(0.5)

    save_button = driver.find_element(
        By.XPATH, "//button[contains(., 'Save settings')]"
    )
    save_button.click()

    success = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'stAlert') and contains(., 'Settings saved')]",
            )
        )
    )
    assert "Settings saved" in success.text
    print("✅ Notification settings test passed!")

    driver.quit()


def move_slider_to_value(driver, slider_element, target_value):
    slider_handle = slider_element.find_element(By.XPATH, ".//*[@role='slider']")
    current_value = int(slider_handle.get_attribute("aria-valuenow"))
    min_value = int(slider_handle.get_attribute("aria-valuemin"))
    max_value = int(slider_handle.get_attribute("aria-valuemax"))

    slider_width = slider_element.size["width"]
    value_range = max_value - min_value
    if value_range == 0:
        raise ValueError("Slider has zero range.")
    move_ratio = (target_value - current_value) / value_range
    x_offset = int(move_ratio * slider_width)

    action = ActionChains(driver)
    action.click_and_hold(slider_handle).move_by_offset(x_offset, 0).release().perform()
