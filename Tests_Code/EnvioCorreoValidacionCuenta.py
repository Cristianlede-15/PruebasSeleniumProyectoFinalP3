from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import shutil
import stat

# Función para manejar errores de permisos
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Función para verificar si la ventana está abierta
def is_window_open(driver):
    try:
        driver.current_window_handle
        return True
    except:
        return False

# Función para tomar capturas de pantalla de página completa
def take_full_page_screenshot(driver, file_path):
    if is_window_open(driver):
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        driver.save_screenshot(file_path)
        driver.set_window_size(original_size['width'], original_size['height'])
    else:
        print('La ventana del navegador está cerrada. No se puede tomar la captura de pantalla.')

# Ruta para el directorio de capturas
screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

# Crear el directorio de capturas si no existe
os.makedirs(screenshots_dir, exist_ok=True)

# Ruta para el directorio específico de este test
envio_correo_test_dir = os.path.join(screenshots_dir, 'EnvioCorreoValidacionCuenta')

# Eliminar el directorio si existe
if os.path.exists(envio_correo_test_dir):
    shutil.rmtree(envio_correo_test_dir, onerror=remove_readonly)

# Crear el directorio
os.makedirs(envio_correo_test_dir, exist_ok=True)

# Inicializar el WebDriver
driver = webdriver.Chrome()

try:
    # Paso 1: Abrir la página de login
    driver.get('http://localhost:3000/auth/login')
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'step1_login_page.png'))

    # Paso 2: Hacer clic en "Registrarse como cliente o delivery"
    register_link = driver.find_element(By.LINK_TEXT, 'Registrarse como cliente o delivery')
    register_link.click()
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'step2_register_page.png'))

    # Paso 3: Completar el formulario de registro
    driver.find_element(By.NAME, 'first_name').send_keys('Juan')
    driver.find_element(By.NAME, 'last_name').send_keys('García')
    driver.find_element(By.NAME, 'email').send_keys('amiircalllof1307@gmail.com')
    driver.find_element(By.NAME, 'username').send_keys('JuanG123')
    driver.find_element(By.NAME, 'password').send_keys('2233')
    driver.find_element(By.NAME, 'confirm_password').send_keys('2233')
    driver.find_element(By.NAME, 'phone').send_keys('+1 849 - 555- 1234')
    driver.find_element(By.NAME, 'profile_image').send_keys(r'C:\Users\pc\Downloads\cena.jpg')
    role_select = Select(driver.find_element(By.NAME, 'role'))
    role_select.select_by_visible_text('Cliente')
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'step3_filled_form.png'))

    # Paso 4: Enviar el formulario
    driver.find_element(By.XPATH, "//button[text()='Registrarse']").click()
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'step4_form_submitted.png'))

    # Esperar la respuesta
    time.sleep(1)
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'step5_registration_result.png'))

except Exception as e:
    print('An error occurred:', e)
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'error.png'))

finally:
    # Cerrar el navegador
    driver.quit()