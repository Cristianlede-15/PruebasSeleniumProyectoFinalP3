import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Function to handle permission errors
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

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

# Path for FormClientesRegistroTest directory
form_clientes_registro_test_dir = os.path.join(screenshots_dir, 'FormClientesRegistroTest')

# Remove FormClientesRegistroTest directory if it exists
if os.path.exists(form_clientes_registro_test_dir):
    shutil.rmtree(form_clientes_registro_test_dir, onerror=remove_readonly)

# Create FormClientesRegistroTest directory
os.makedirs(form_clientes_registro_test_dir, exist_ok=True)

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the login page
    driver.get('http://localhost:3000/auth/login')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step1_login_page.png'))

    # Step 2: Click on "Registrarse como cliente o delivery"
    register_link = driver.find_element(By.LINK_TEXT, 'Registrarse como cliente o delivery')
    register_link.click()
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step2_register_page.png'))

    # Step 3: Fill out the registration form
    driver.find_element(By.NAME, 'first_name').send_keys('Luis')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step3_first_name.png'))

    driver.find_element(By.NAME, 'last_name').send_keys('Perez')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step4_last_name.png'))

    driver.find_element(By.NAME, 'email').send_keys('setitay970@nausard.com')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step5_email.png'))

    driver.find_element(By.NAME, 'username').send_keys('LuisitoPerez777')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step6_username.png'))

    driver.find_element(By.NAME, 'password').send_keys('2233')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step7_password.png'))

    driver.find_element(By.NAME, 'confirm_password').send_keys('2233')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step8_confirm_password.png'))

    driver.find_element(By.NAME, 'phone').send_keys('+1 849 - 555- 7788')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step9_phone.png'))

    driver.find_element(By.NAME, 'profile_image').send_keys(r'C:\Users\pc\Downloads\cena.jpg')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step10_profile_image.png'))

    # Step 4: Select role
    role_select = Select(driver.find_element(By.NAME, 'role'))
    role_select.select_by_visible_text('Cliente')
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step11_role_selected.png'))

    # Step 5: Submit the form
    driver.find_element(By.XPATH, "//button[text()='Registrarse']").click()
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step12_form_submitted.png'))

    # Wait for response
    time.sleep(5)
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'step13_registration_result.png'))

    # Add assertions here if needed

except Exception as e:
    print('An error occurred:', e)
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'error.png'))

finally:
    # Close the browser
    driver.quit()