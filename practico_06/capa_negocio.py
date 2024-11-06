# Implementar los metodos de la capa de negocio de socios.

# Añadir el directorio padre al sys.path
import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar módulos de practico_05
from practico_05.ejercicio_01 import Socio
from practico_05.ejercicio_02 import DatosSocio


class DniRepetido(Exception):
    pass


class LongitudInvalida(Exception):
    pass


class MaximoAlcanzado(Exception):
    pass


class NegocioSocio(object):

    MIN_CARACTERES = 3
    MAX_CARACTERES = 15
    MAX_SOCIOS = 200

    def __init__(self):
        self.datos = DatosSocio()

    def buscar(self, id_socio):
        """
        Devuelve la instancia del socio, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar(id_socio)

    def buscar_dni(self, dni_socio):
        """
        Devuelve la instancia del socio, dado su dni.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar_dni(dni_socio)

    def todos(self):
        """
        Devuelve listado de todos los socios.
        :rtype: list
        """
        return self.datos.todos()

    def alta(self, socio):
        """
        Da de alta un socio.
        Se deben validar las 3 reglas de negocio primero.
        Si no validan, levantar la excepcion correspondiente.
        Devuelve True si el alta fue exitoso.
        :type socio: Socio
        :rtype: bool
        """
        if not self.regla_1(socio):
            raise DniRepetido(f"El DNI {socio.dni} ya está registrado.")
        
        if not self.regla_2(socio):
            raise LongitudInvalida(f"El nombre y apellido deben tener entre {self.MIN_CARACTERES} y {self.MAX_CARACTERES} caracteres.")
        
        if not self.regla_3():
            raise MaximoAlcanzado(f"El número máximo de socios ({self.MAX_SOCIOS}) ha sido alcanzado.")

        return self.datos.alta(socio) is not None

    def baja(self, id_socio):
        """
        Borra el socio especificado por el id.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        return self.datos.baja(id_socio)

    def modificacion(self, socio):
        """
        Modifica un socio.
        Se debe validar la regla 2 primero.
        Si no valida, levantar la excepcion correspondiente.
        Devuelve True si la modificacion fue exitosa.
        :type socio: Socio
        :rtype: bool
        """
        if not self.regla_2(socio):
            raise LongitudInvalida(f"El nombre y apellido deben tener entre {self.MIN_CARACTERES} y {self.MAX_CARACTERES} caracteres.")
        
        return self.datos.modificacion(socio) is not None

    def regla_1(self, socio):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        existing_socio = self.datos.buscar_dni(socio.dni)
        return existing_socio is None

    def regla_2(self, socio):
        """
        Validar que el nombre y el apellido del socio cuenten con mas de 3 caracteres pero menos de 15.
        :type socio: Socio
        :raise: LongitudInvalida
        :return: bool
        """
        return (self.MIN_CARACTERES <= len(socio.nombre) <= self.MAX_CARACTERES and
                self.MIN_CARACTERES <= len(socio.apellido) <= self.MAX_CARACTERES)

    def regla_3(self):
        """
        Validar que no se esta excediendo la cantidad maxima de socios.
        :raise: MaximoAlcanzado
        :return: bool
        """
        return self.datos.contarSocios() < self.MAX_SOCIOS