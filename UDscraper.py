import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

# Underdog may change their websites design so you
# may need to update XPaths for the scraper to work 


# Function to introduce random delays
def random_delay(start=1, end=2):
    time.sleep(random.uniform(start, end))

# Path to your extracted Microsoft Edge driver executable
edge_driver_path = r'C:\Users\lukem\Downloads\edgedriver_win64\msedgedriver.exe'

# Initialize the Edge WebDriver with the correct Service object and options
edge_options = Options()
edge_options.add_argument("start-maximized")
edge_options.add_argument("disable-blink-features=AutomationControlled")

service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# Set headers to mimic a real user
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

driver.get("https://underdogfantasy.com/")
print("Page title is: %s" % driver.title)

try:
    print("Waiting for login button...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/button[1]")))
    random_delay()
    print("Clicking Login button...")
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/button[1]").click()
    random_delay()
except TimeoutException as e:
    print("Timeout waiting for the login button: ", e)

# Enter credentials and login
try:
    print("Entering credentials...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/div[1]/label/div[2]/input")))
    
    email_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/div[1]/label/div[2]/input")
    password_field = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/div[2]/label/div[2]/input")
    
    email_field.send_keys("lukemast22@gmail.com")
    print("Entered email")
    random_delay()

    password_field.send_keys("Hockeyislife#12")
    print("Entered password")
    random_delay()

    print("Submitting login form...")
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/button[2]").click()
    random_delay()
except TimeoutException as e:
    print("Timeout waiting for the login form: ", e)
except NoSuchElementException as e:
    print("Error finding element: ", e)
except Exception as e:
    print("An error occurred: ", e)

ppPlayers = []

try:
    print("Selecting MLB...")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "MLB")))

    driver.find_element(By.ID, "MLB").click()
    random_delay()

    print("Checking strikeout category...")
    categories = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "styles__currentStat__S6U2b"))
    )

    print("Getting player names...")
    names = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "styles__playerName__Coe_G")))

    for i, cat in enumerate(categories):
        if "Strikeouts" in cat.text:
            strikeout_value = cat.text.split('\n')[0]  # Extracting just the numeric value
            player_name = names[i].text if i < len(names) else "Unknown"
            
            players = {
                'Name': player_name,
                'Value': cat.text,
                'Strikeouts': strikeout_value
            }
            ppPlayers.append(players)

    print("Waiting for projections...")
    projectionsPP = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection"))
    )

    for projections in projectionsPP:
        try:
            names = projections.find_element(By.CLASS_NAME, "name").text
            value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
            proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

            players = {
                'Name': names,
                'Value': value,
                'Prop': proptype.replace("<wbr>", "")
            }
            ppPlayers.append(players)
        except NoSuchElementException:
            print("An element was not found, skipping to the next.")

except TimeoutException as e:
    print("Timeout waiting for the elements: ", e)
except Exception as e:
    print("An error occurred: ", e)

dfProps = pd.DataFrame(ppPlayers)

# Sort DataFrame by 'Strikeouts' column
dfProps_sorted = dfProps.sort_values(by='Strikeouts')

# Save the sorted DataFrame to CSV
dfProps_sorted.to_csv('sorted_strikeout_projections.csv', index=False)

print("Sorted strikeout projections saved to 'sorted_strikeout_projections.csv'.")
print(dfProps_sorted)

# Close the driver
driver.quit()
