from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.nytimes.com/games/wordle/index.html")

# Close cookies pop-up
driver.find_element_by_id("pz-gdpr-btn-closex").click()
