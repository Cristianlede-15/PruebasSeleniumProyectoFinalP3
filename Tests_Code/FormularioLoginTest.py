import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
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

# Path for FormularioLoginTest directory
formulario_login_test_dir = os.path.join(screenshots_dir, 'FormularioLoginTest')

# Remove FormularioLoginTest directory if it exists
if os.path.exists(formulario_login_test_dir):
    shutil.rmtree(formulario_login_test_dir, onerror=remove_readonly)

# Create FormularioLoginTest directory
os.makedirs(formulario_login_test_dir, exist_ok=True)

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the login page
    driver.get('http://localhost:3000/auth/login')
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step1_login_page.png'))

    # Step 2: Enter username and password
    driver.find_element(By.ID, 'identifier').send_keys('Man')
    driver.find_element(By.ID, 'password').send_keys('2233')
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step2_credentials_entered.png'))

    # Step 3: Click on "¿Olvidaste tu contraseña?"
    forgot_password_link = driver.find_element(By.LINK_TEXT, '¿Olvidaste tu contraseña?')
    forgot_password_link.click()
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step3_forgot_password.png'))
    driver.back()
    time.sleep(1)

    # Step 4: Click on "Registrarse como cliente o delivery"
    register_client_link = driver.find_element(By.LINK_TEXT, 'Registrarse como cliente o delivery')
    register_client_link.click()
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step4_register_client.png'))
    driver.back()
    time.sleep(1)

    # Step 5: Click on "Registrar comercio"
    register_business_link = driver.find_element(By.LINK_TEXT, 'Registrar comercio')
    register_business_link.click()
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step5_register_business.png'))
    driver.back()
    time.sleep(1)

    # Step 6: Log in
    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step6_logged_in.png'))

    # Wait for response
    time.sleep(5)
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'step7_final_state.png'))

except Exception as e:
    print('An error occurred:', e)
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'error.png'))

finally:
    # Close the browser
    driver.quit()