import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_buscar_region_kalos(driver):
    driver.get("http://localhost:3000/")
    if not os.path.exists('screenshots/test_buscar_regionPokemon'):
        os.makedirs('screenshots/test_buscar_regionPokemon')
    driver.save_screenshot('screenshots/test_buscar_regionPokemon/AbrirPagina.png')

    select_region = Select(driver.find_element(By.NAME, "region"))
    driver.save_screenshot('screenshots/test_buscar_regionPokemon/BuscarElementoBuscarSelect.png')
    select_region.select_by_visible_text("Kalos")
    driver.save_screenshot('screenshots/test_buscar_regionPokemon/SeleccionarRegionABuscar.png')
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    driver.save_screenshot('screenshots/test_buscar_regionPokemon/EnviarSolicitudBuscar.png')
    assert "Kalos" in driver.page_source
    driver.save_screenshot('screenshots/test_buscar_regionPokemon/RegionEncontrada.png')