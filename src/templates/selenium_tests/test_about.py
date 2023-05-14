from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

driver.get('file:///C:/Users/johnm/Documents/repo/ISEmodules/CS4442/SoftwareTestingProject/4442Testing/src/templates/about.html') 

try:
    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'h5'))
    )

    # Assert that the heading text is correct
    assert heading.text == 'About Page'

    # Print a success message if the test passed
    print('Test Passed: Heading text is correct')

except Exception as e:
    # Print an error message if the test failed
    print('Test Failed: ', str(e))

finally:
    # Close the browser
    driver.quit()
