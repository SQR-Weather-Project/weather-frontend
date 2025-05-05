from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_history():
    driver = webdriver.Chrome(service=Service())
    driver.get("http://localhost:8501/History")

    wait = WebDriverWait(driver, 15)

    country_select = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[contains(., 'Country')]/following-sibling::div"
    )))
    country_select.click()
    option_ru = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[text()='RU']")))
    option_ru.click()

    city_select = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//label[contains(., 'City')]/following-sibling::div"
    )))
    city_select.click()
    option_msc = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "//div[text()='Moscow']")))
    option_msc.click()

    date_select = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//label[contains(., 'Date')]/following-sibling::div"
    )))
    date_select.click()
    option_2025_04_22 = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "//div[text()='2025-04-22']")))
    option_2025_04_22.click()

    time_select = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//label[contains(., 'Time')]/following-sibling::div"
    )))
    time_select.click()
    option_all = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "//div[text()='All']")))
    option_all.click()

    expected_text = "Showing data for Moscow, RU on 2025-04-22 at all times."
    element = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((
            By.CSS_SELECTOR,
            "div[data-testid='stCaptionContainer'] > p"),
            expected_text
        )
    )
    assert element, "Expected text not found in the caption container!"

    print("✅ Test passed: The expected caption is visible.")
    driver.quit()
