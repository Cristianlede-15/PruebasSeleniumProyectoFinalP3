import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_crear_region(driver):
    driver.get("http://localhost:3000/regiones/new")
    if not os.path.exists('screenshots/test_crearRegion'):
        os.makedirs('screenshots/test_crearRegion')
    driver.save_screenshot('screenshots/test_crearRegion/AbrirPagina.png')

    wait = WebDriverWait(driver, 10)

    nombre = wait.until(EC.presence_of_element_located((By.ID, "nombre")))
    nombre.send_keys("Juan")
    driver.save_screenshot('screenshots/test_crearRegion/IngresarNombre.png')

    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()
    driver.save_screenshot('screenshots/test_crearRegion/EnviarFormulario.png')

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list-group")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.save_screenshot('screenshots/test_crearRegion/PgDn.png')

    assert "Juan" in driver.page_source
    driver.save_screenshot('screenshots/test_crearRegion/RegionCreada.png')