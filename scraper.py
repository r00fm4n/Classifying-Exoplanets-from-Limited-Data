"""
Scraper for retreving exoplanet labels from nasa website
Written with help from genaretive AI
authur: Emil Takman
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the driver
driver = webdriver.Chrome()
driver.get("https://science.nasa.gov/exoplanets/exoplanet-catalog/")

wait = WebDriverWait(driver, 15)

# Define filters with checkbox IDs and output filenames
filters = {
    "checkbox-acf_planet_type_terrestrial-Terrestrial": "terrestrial.txt",
    "checkbox-acf_planet_type_super earth-Super Earth": "super_earth.txt",
    "checkbox-acf_planet_type_neptune-like-Neptune-like": "neptune_like.txt",
    "checkbox-acf_planet_type_gas giant-Gas Giant": "gas_giant.txt",
}

for checkbox_id, filename in filters.items():
    # Refresh page for a clean filter start
    driver.get("https://science.nasa.gov/exoplanets/exoplanet-catalog/")
    wait.until(EC.presence_of_element_located((By.ID, checkbox_id)))

    # Click the filter checkbox
    checkbox = driver.find_element(By.ID, checkbox_id)
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)  # give results time to load

    results = []

    while True:
        # Collect planet names on the current page
        names = driver.find_elements(By.CSS_SELECTOR, "div.hds-a11y-heading-22")
        for n in names:
            results.append(n.text.strip())

        # Try to click "Next"
        try:
            next_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next.page-numbers"))
            )
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(3)  # wait for page load
        except:
            # No more pages
            break

    # Save to txt file
    with open(filename, "w", encoding="utf-8") as f:
        for item in results:
            f.write(item + "\n")

    print(f"Saved {len(results)} planets to {filename}")

driver.quit()
