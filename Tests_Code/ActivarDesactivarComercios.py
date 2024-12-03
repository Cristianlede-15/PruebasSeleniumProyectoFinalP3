import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

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
activar_desactivar_comercios_dir = os.path.join(screenshots_dir, 'ActivarDesactivarComercios')

# Eliminar el directorio si existe
if os.path.exists(activar_desactivar_comercios_dir):
    shutil.rmtree(activar_desactivar_comercios_dir, onerror=remove_readonly)

# Crear el directorio
os.makedirs(activar_desactivar_comercios_dir, exist_ok=True)

# Inicializar el WebDriver
driver = webdriver.Chrome()

# Maximizar la ventana del navegador
driver.maximize_window()

try:
    # Paso 1: Abrir la página de login
    driver.get('http://localhost:3000/auth/login')
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step1_login_page.png'))

    # Paso 2: Ingresar credenciales de administrador
    driver.find_element(By.ID, 'identifier').send_keys('Admin')
    driver.find_element(By.ID, 'password').send_keys('3322')
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step2_credentials_entered.png'))

    # Paso 3: Enviar el formulario de login
    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step3_login_submitted.png'))

    # Esperar a que la página de dashboard cargue
    time.sleep(3)
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step4_dashboard_loaded.png'))

    # Paso 4: Navegar a "Comercios"
    comercios_link = driver.find_element(By.LINK_TEXT, 'Comercios')
    comercios_link.click()
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step5_comercios_page.png'))

    # Esperar a que la página de comercios cargue
    time.sleep(3)

    # Paso 5: Inactivar un comercio
    # Selecciona el primer comercio en la lista
    comercio = driver.find_element(By.CSS_SELECTOR, '.commerce')
    inactivar_button = comercio.find_element(By.CSS_SELECTOR, 'button.btn-warning')
    inactivar_button.click()
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step6_comercio_inactivado.png'))

    # Esperar a que la acción se complete
    time.sleep(2)

    # Paso 6: Activar el mismo comercio
    comercio = driver.find_element(By.CSS_SELECTOR, '.commerce')
    activar_button = comercio.find_element(By.CSS_SELECTOR, 'button.btn-success')
    activar_button.click()
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'step7_comercio_activado.png'))

    # Esperar a que la acción se complete
    time.sleep(2)

except Exception as e:
    print('An error occurred:', e)
    take_full_page_screenshot(driver, os.path.join(activar_desactivar_comercios_dir, 'error.png'))

finally:
    # Cerrar el navegador
    driver.quit()