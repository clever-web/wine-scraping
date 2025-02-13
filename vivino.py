import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
# options = Options()
# options.add_argument("--headless")  # Run headless
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Disable automation controls
options.add_experimental_option("useAutomationExtension", False)  # Disable use of automation extensions

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open Vivino Singapore page
driver.get("https://www.vivino.com/explore?e=eJzLLbI1VMvNzAORiRW2ZkamasmVtsXpasm2we4uagVA8fQ027LEoszUksQctfyiFNuU1OJktfykStuixJLMvPTi-MSy1KLE9FS18pLoWKB6MGUEoYwhlAmEMofKmQAAH18nZg%3D%3D")
time.sleep(5)  # Wait for page to load

# Accept Cookies if prompted
try:
    # cookie_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Agree')]")
    cookie_btn = driver.find_element(By.ID, "didomi-notice-agree-button")
    cookie_btn.click()
    print("btn clicked")
    time.sleep(3)
except:
    pass  # No cookies popup

# Scroll down function
def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Extract Wine Data
def get_wines():
    wines = []
    wine_elements = driver.find_elements(By.CSS_SELECTOR, "div.explorerPageResults__resultsWrapper--2xwUf")
    print("wines", wine_elements)
    for wine in wine_elements:
        print("wine", wine)
        try:
            name = wine.find_element(By.CSS_SELECTOR, "div.wineInfoVintage__truncate--3QAtw").text
            # price = wine.find_element(By.CSS_SELECTOR, "div.price").text
            price = driver.find_element(By.XPATH, "//div[contains(@class, 'addToCartButton__price')]/div[last()]").text
            rating = wine.find_element(By.CSS_SELECTOR, "div.rating-average").text
            wines.append({"Name": name, "Price": price, "Rating": rating})
        except:
            continue

    return wines

# Pagination Loop
all_wines = []
page = 1

while (page < 3):
    print(f"Scraping Page {page}...")
    scroll_down()
    all_wines.extend(get_wines())

    try:
        # next_button = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
        next_button = driver.find_element(By.XPATH, "//div[contains(@class, 'explorerPagination-module__next')]//a")
        if "Mui-disabled" in next_button.get_attribute("class") or next_button.get_attribute("aria-disabled") == "true":
            break  # Stop if the next button is disabled
        next_button.click()
        time.sleep(5)
        page += 1
    except:
        break  # No more pages

# Save data to CSV
df = pd.DataFrame(all_wines)
df.to_csv("vivino_wines_singapore.csv", index=False)

# Close browser
driver.quit()

print("Scraping completed. Data saved in 'vivino_wines_singapore.csv'.")
