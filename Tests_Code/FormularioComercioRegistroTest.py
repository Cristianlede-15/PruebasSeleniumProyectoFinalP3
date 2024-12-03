from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
import stat

# Function to take full-page screenshots
def take_full_page_screenshot(driver, file_path):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(file_path)
    driver.set_window_size(original_size['width'], original_size['height'])

# Path for screenshots directory
screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

# Create the screenshots directory if it doesn't exist
os.makedirs(screenshots_dir, exist_ok=True)

# Path for FormRegistroTest directory
form_registro_test_dir = os.path.join(screenshots_dir, 'FormRegistroTest')

# Remove FormRegistroTest directory if it exists
if os.path.exists(form_registro_test_dir):
    # Change the permissions of the directory
    for root, dirs, files in os.walk(form_registro_test_dir):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IWUSR)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IWUSR)
    shutil.rmtree(form_registro_test_dir)

# Create FormRegistroTest directory
os.makedirs(form_registro_test_dir)

# Initialize the WebDriver
driver = webdriver.Chrome()

# Maximize the browser window

try:
    # Step 1: Open the login page
    driver.get('http://localhost:3000/auth/login')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step1_login_page.png'))

    # Step 2: Click on "Registrar comercio"
    register_link = driver.find_element(By.LINK_TEXT, 'Registrar comercio')
    register_link.click()
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step2_register_page.png'))

    # Step 3: Fill out the registration form
    driver.find_element(By.ID, 'business_name').send_keys('Comedor Maria')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step3_business_name.png'))

    driver.find_element(By.ID, 'phone').send_keys('+1 809-888-9999')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step4_phone.png'))

    driver.find_element(By.ID, 'email').send_keys('setitay970@nausard.com')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step5_email.png'))

    driver.find_element(By.ID, 'logo').send_keys(r'C:\Users\pc\Downloads\logorestaurante.webp')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step6_logo.png'))

    # Step 4: Set opening and closing times using JavaScript
    driver.execute_script("document.getElementById('opening_time').value = '08:00'")
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step7_opening_time.png'))

    driver.execute_script("document.getElementById('closing_time').value = '21:00'")
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step8_closing_time.png'))

    # Step 5: Select business type
    business_type_element = driver.find_element(By.ID, 'business_type')
    options = business_type_element.find_elements(By.TAG_NAME, 'option')
    for option in options:
        print('Available option:', option.text)
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step9_business_type_options.png'))

    # Initialize Select class
    business_type = Select(business_type_element)
    # Use the exact text from the options printed
    business_type.select_by_visible_text('Restaurantes')  # Adjust if necessary
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step10_business_type_selected.png'))

    # Step 6: Enter password
    driver.find_element(By.ID, 'password').send_keys('2233')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step11_password.png'))

    driver.find_element(By.ID, 'confirm_password').send_keys('2233')
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step12_confirm_password.png'))

    # Step 7: Submit the form
    driver.find_element(By.XPATH, "//button[text()='Registrar Comercio']").click()
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step13_form_submitted.png'))

    # Wait for response
    time.sleep(5)
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'step14_registration_result.png'))

    # Add assertions here if needed

except Exception as e:
    print('An error occurred:', e)
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'error.png'))

finally:
    # Close the browser
    driver.quit()