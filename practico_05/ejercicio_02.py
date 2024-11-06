"""Base de Datos - ORM"""

import sys
import os

# Añadir el directorio raíz del proyecto para que practico_05 sea accesible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from practico_05.ejercicio_01 import Base, Socio
from typing import List, Optional

class DatosSocio():

    def __init__(self):
        self.engine = create_engine("sqlite:///:memory:", echo=False) # Crea BD SQLite persistente
        Base.metadata.create_all(self.engine) # Crea las tablas definidas en "Base"
        self.Session = sessionmaker(bind=self.engine)

    def buscar(self, id_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su id. Devuelve None si no encuentra nada."""
        session = self.Session()
        socio = session.query(Socio).filter_by(id_socio=id_socio).first()
        session.close()
        return socio

    def buscar_dni(self, dni_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su dni. Devuelve None si no encuentra nada."""
        session = self.Session()
        socio = session.query(Socio).filter_by(dni=dni_socio).first()
        session.close()
        return socio
        
    def todos(self) -> List[Socio]:
        """Devuelve listado de todos los socios en la base de datos."""
        session = self.Session()
        socios = session.query(Socio).all()
        session.close()
        return socios

    def borrar_todos(self) -> bool:
        """Borra todos los socios de la base de datos. Devuelve True si el borrado fue exitoso."""
        session = self.Session()
        try:
            session.query(Socio).delete()
            session.commit()
            success = True
        except:
            session.rollback()
            success = False
        finally:
            session.close()
        return success

    def alta(self, socio: Socio) -> Socio:
        """Agrega un nuevo socio a la tabla y lo devuelve"""
        session = self.Session()
        try:
            session.add(socio)
            session.commit()
            session.refresh(socio)  # Actualiza el objeto socio para obtener su ID autogenerado
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return socio

    def baja(self, id_socio: int) -> bool:
        """Borra el socio especificado por el id. Devuelve True si el borrado fue exitoso. """
        session = self.Session()
        try:
            socio = session.query(Socio).filter_by(id_socio=id_socio).first()
            if socio:
                session.delete(socio)
                session.commit()
                success = True
            else:
                success = False
        except:
            session.rollback()
            success = False
        finally:
            session.close()
        return success

    def modificacion(self, socio: Socio) -> Socio:
        """Guarda un socio con sus datos modificados. Devuelve el Socio modificado. """
        session = self.Session()
        try:
            # Realiza la actualización de los datos del socio ya existente
            existing_socio = session.query(Socio).filter_by(id_socio=socio.id_socio).first()
            if existing_socio:
                existing_socio.dni = socio.dni
                existing_socio.nombre = socio.nombre
                existing_socio.apellido = socio.apellido
                session.commit()
                session.refresh(existing_socio)  # Asegura que el objeto tenga los datos más recientes de la BD
            else:
                raise ValueError("El socio especificado no existe.")
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return existing_socio
    
    def contarSocios(self) -> int:
        """Devuelve el total de socios que existen en la tabla"""
        session = self.Session()
        count = session.query(Socio).count()
        session.close()
        return count



# NO MODIFICAR - INICIO

# Test Creación
datos = DatosSocio()

# Test Alta
socio = datos.alta(Socio(dni=12345678, nombre='Juan', apellido='Perez'))
assert socio.id_socio > 0

# Test Baja
assert datos.baja(socio.id_socio) == True

# Test Consulta
socio_2 = datos.alta(Socio(dni=12345679, nombre='Carlos', apellido='Perez'))
socio_encontrado = datos.buscar(socio_2.id_socio)
assert socio_encontrado.id_socio == socio_2.id_socio
assert socio_encontrado.dni == socio_2.dni
assert socio_encontrado.nombre == socio_2.nombre
assert socio_encontrado.apellido == socio_2.apellido

# Test Buscar DNI
socio_2 = datos.alta(Socio(dni=12345670, nombre='Carlos', apellido='Perez'))
socio_encontrado = datos.buscar_dni(socio_2.dni)
assert socio_encontrado.id_socio == socio_2.id_socio
assert socio_encontrado.dni == socio_2.dni
assert socio_encontrado.nombre == socio_2.nombre
assert socio_encontrado.apellido == socio_2.apellido

# Test Modificación
socio_3 = datos.alta(Socio(dni=12345680, nombre='Susana', apellido='Gimenez'))
socio_3.nombre = 'Moria'
socio_3.apellido = 'Casan'
socio_3.dni = 13264587
datos.modificacion(socio_3)
socio_3_modificado = datos.buscar(socio_3.id_socio)
assert socio_3_modificado.id_socio == socio_3.id_socio
assert socio_3_modificado.nombre == 'Moria'
assert socio_3_modificado.apellido == 'Casan'
assert socio_3_modificado.dni == 13264587

# Test Conteo
assert len(datos.todos()) == 3

# Test Delete
datos.borrar_todos()
assert len(datos.todos()) == 0

# NO MODIFICAR - FIN
