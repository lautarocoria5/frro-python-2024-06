# scraping_script.py
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from app import db
from app.models import Inmueble

def scrape_inmuebles():
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)

    base_url = 'https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/santa-fe/rosario/'
    page = 1

    try:
        while True:
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}_Desde_{(page-1)*50 + 1}"

            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-result__wrapper')))
            listings = driver.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper')

            if not listings:
                break

            for listing in listings:
                try:
                    title_element = listing.find_element(By.CSS_SELECTOR, 'a.ui-search-link__title-card.ui-search-link h2.ui-search-item__title')
                    title = title_element.text
                    price_element = listing.find_element(By.CSS_SELECTOR, '.ui-search-price .andes-money-amount__fraction')
                    price = price_element.text
                    location_element = listing.find_element(By.CSS_SELECTOR, '.ui-search-item__location-container-grid .ui-search-item__location-label')
                    location = location_element.text
                    link_element = listing.find_element(By.CSS_SELECTOR, 'a.ui-search-link__title-card.ui-search-link')
                    link = link_element.get_attribute('href')

                    # Convertir precio a float
                    price = float(price.replace('.', '').replace(',', '.'))

                    # Crear un nuevo registro en la base de datos
                    inmueble = Inmueble(title=title, price=price, location=location, link=link)
                    db.session.add(inmueble)
                    db.session.commit()
                except Exception as e:
                    print(f"Ocurrió un error al procesar un listado: {e}")

            page += 1
    finally:
        driver.quit()
