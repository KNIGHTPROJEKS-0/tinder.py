import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def get_undetected_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 12; Pixel 5 Build/SP1A.210812.015) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"
    )

    # Not headless to avoid detection
    driver = uc.Chrome(options=options)
    return driver
