from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import re
import logging
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Configurar el servicio de GeckoDriver
service = FirefoxService(executable_path=GeckoDriverManager().install())

# Crear una instancia de Firefox con GeckoDriver
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Ejecutar Firefox en modo headless
driver = webdriver.Firefox(service=service, options=options)

# URL de la página web de inmuebles en MercadoLibre
base_url = 'https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/santa-fe/rosario/'
page = 1

# Lista para almacenar los datos de los inmuebles
inmuebles_data = []

try:
    while True:
        url = base_url if page == 1 else f"{base_url}_Desde_{(page - 1) * 50 + 1}"
        print(f"Accediendo a la URL: {url}")

        driver.get(url)
        time.sleep(5)
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-layout__item')))
        except TimeoutException:
            print("Timeout: No se encontraron elementos en el tiempo especificado.")
            break

        listings = driver.find_elements(By.CLASS_NAME, 'ui-search-layout__item')

        if not listings:
            print("No se encontraron listados, se detiene la extracción.")
            break

        def clean_price(price_text):
            """Limpia y convierte el texto del precio a float."""
            if price_text:
                try:
                    price_text = re.sub(r'[^\d,]', '', price_text)
                    if ',' in price_text:
                        price_text = price_text.replace('.', '').replace(',', '.')
                    price_value = float(price_text)
                    return price_value if price_value > 0 else None
                except ValueError as e:
                    print(f"Error al convertir a float: '{price_text}': {e}")
                    return None
            return None

        def extract_value(element, keyword):
            """Extrae el valor correspondiente a un keyword del elemento."""
            try:
                values = element.find_elements(By.CSS_SELECTOR, 'li.poly-attributes-list__item')
                value_text = next((el.text for el in values if keyword in el.text), None)
                return int(value_text.split(' ')[0]) if value_text else None
            except Exception as e:
                print(f'Error al extraer {keyword}: {e}')
                return None

        for listing in listings:
            try:
                title_element = listing.find_element(By.CSS_SELECTOR, 'h2')
                title = title_element.text

                price_element = listing.find_element(By.CSS_SELECTOR, 'span.andes-money-amount__fraction')
                price_value = clean_price(price_element.text.strip() if price_element else None)

                location_element = listing.find_element(By.CSS_SELECTOR, 'span.poly-component__location')
                location = location_element.text
                link_element = listing.find_element(By.CSS_SELECTOR, 'a')
                link = link_element.get_attribute('href')

                print(f'Título: {title}, Precio: {price_value}, Ubicación: {location}, Link: {link}')
                # ---------------- ult prueba de extraccion ---------------------------
                # Extraer ambientes usando un selector CSS
                ambientes_element = listing.find_element(By.XPATH, ".//li[contains(text(), 'amb.')] | .//li[contains(text(), 'ambs.')]")
                ambientes_value = int(re.search(r'\d+', ambientes_element.text).group()) if ambientes_element else 0

                # Extraer baños usando un selector CSS
                banos_element = listing.find_element(By.XPATH, ".//li[contains(text(), 'baño')]")
                banos_value = int(re.search(r'\d+', banos_element.text).group()) if banos_element else 0

                # Extraer metros cuadrados usando un selector CSS
                metros_element = listing.find_element(By.XPATH, ".//li[contains(text(), 'm²')]")
                metros_value = float(re.search(r'[\d,]+', metros_element.text).group().replace(',', '.')) if metros_element else 0.0
                # # Extraer ambientes
                # ambientes_value = extract_value(listing, ['amb.', 'ambs.']) or 0

                # # Extraer baños
                # banos_value = extract_value(listing, ['baño', 'baños']) or 0

                # # Extraer metros cuadrados
                # metros_element = listing.find_elements(By.CSS_SELECTOR, 'li.poly-attributes-list__item')
                # metros_text = next((el.text for el in metros_element if 'm²' in el.text), None)
                # metros_value = float(metros_text.split(' ')[0].replace(',', '.')) if metros_text else 0.0
                #-----------------------------------------------------------------------------
                # Solo agregar inmuebles con precios válidos
                if price_value is not None:
                    inmueble_data = {
                        'title': title,
                        'price': price_value,
                        'location': location,
                        'ambientes': ambientes_value,
                        'banos': banos_value,
                        'metros_cuadrados': metros_value,
                        'link': link
                    }
                    inmuebles_data.append(inmueble_data)

            except Exception as e:
                print(f'Error al procesar el listado: {e}')

        page += 1

except Exception as e:
    print(f'Error en el script principal: {e}')
    import traceback
    traceback.print_exc()

finally:
    driver.quit()

# Crear un DataFrame con los datos recolectados
df_inmuebles = pd.DataFrame(inmuebles_data)

# Guardar el DataFrame en un archivo CSV
df_inmuebles.to_csv('inmuebles.csv', index=False)

print("Datos guardados en inmuebles.csv")
