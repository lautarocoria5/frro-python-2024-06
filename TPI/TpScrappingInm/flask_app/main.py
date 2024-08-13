from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from app import db, create_app
from app.models import Inmueble

# Crear la aplicación y empujar el contexto de aplicación
app = create_app()

# Usar el contexto de la aplicación para las operaciones de base de datos
with app.app_context():
    # Configurar el servicio de GeckoDriver
    service = FirefoxService(executable_path=GeckoDriverManager().install())

    # Crear una instancia de Firefox con GeckoDriver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Ejecutar Firefox en modo headless
    driver = webdriver.Firefox(service=service, options=options)

    # URL de la página web de inmuebles en MercadoLibre
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
                print("No se encontraron listados, se detiene la extracción.")
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

                    # Depuración de precios
                    print(f'Precio extraído: {price}')

                    try:
                        ambientes_element = listing.find_element(By.XPATH, './/li[contains(text(), "ambs.") or contains(text(), "amb.") or contains(text(), "ambiente") or contains(text(), "ambientes")]')
                        ambientes_text = ambientes_element.text
                        ambientes_value = int(ambientes_text.split(' ')[0]) if ambientes_text else None
                    except Exception:
                        ambientes_value = None

                    try:
                        banos_element = listing.find_element(By.XPATH, './/li[contains(text(), "baño") or contains(text(), "baños")]')
                        banos_text = banos_element.text
                        banos_value = int(banos_text.split(' ')[0]) if banos_text else None
                    except Exception:
                        banos_value = None

                    try:
                        metros_element = listing.find_element(By.XPATH, './/li[contains(text(), "m²")]')
                        metros_text = metros_element.text
                        metros_value = float(metros_text.split(' ')[0].replace(',', '.')) if metros_text else None
                    except Exception:
                        metros_value = None

                    # Convertir el precio a float
                    try:
                        price_value = float(price.replace('.', '').replace(',', '.'))
                    except ValueError:
                        price_value = None  # Si el precio no es convertible, asignar None

                    if price_value is not None:  # Solo agregar inmuebles con precios válidos
                        inmueble = Inmueble(
                            title=title,
                            price=price_value,
                            location=location,
                            link=link,
                            ambientes=ambientes_value,
                            banos=banos_value,
                            metros_cuadrados=metros_value
                        )

                        try:
                            db.session.add(inmueble)
                            db.session.commit()
                            print(f'Agregado: {title} - ${price_value}')
                        except Exception as e:
                            db.session.rollback()
                            print(f'Error al insertar registro: {e}')
                    else:
                        print(f'Precio inválido para el inmueble: {title}')
                        
                except Exception as e:
                    print(f'Error al extraer datos del listado: {e}')

            page += 1

    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()
