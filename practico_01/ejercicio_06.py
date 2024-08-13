"""Type, Comprensión de Listas, Sorted y Filter."""

from typing import List, Union


def numeros_al_final_basico(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Toma una lista de enteros y strings y devuelve una lista con todos los
    elementos numéricos al final.
    """
    pass # Completar
    cad=[]
    enteros=[]
    for c in lista:
        if type(c) == str:
            cad.append(c)
        else:
            enteros.append(c)
    return cad + enteros    


# NO MODIFICAR - INICIO
assert numeros_al_final_basico([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_comprension(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando comprensión de listas."""
    pass # Completar

    cad2  = [c for c in lista if type(c) == str]
    entero2 = [c for c in lista if type(c) != str]
    return cad2 + entero2

# NO MODIFICAR - INICIO
assert numeros_al_final_comprension([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_sorted(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando la función sorted con una custom key.
    Referencia: https://docs.python.org/3/library/functions.html#sorted
    """
    pass # Completar
    cad3 = []
    entero3 = []
    def custom_key(element):
        if type(element)==str:
            cad3.append(element)
            return 0
        else:
            entero3.append(element)
            return 1

    return sorted(lista, key=custom_key)


# NO MODIFICAR - INICIO
assert numeros_al_final_sorted([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_filter(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """CHALLENGE OPCIONAL - Re-escribir utilizando la función filter.
    Referencia: https://docs.python.org/3/library/functions.html#filter
    """
    pass # Completar


# NO MODIFICAR - INICIO
if __name__ == "__main__":
    assert numeros_al_final_filter([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_recursivo(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """CHALLENGE OPCIONAL - Re-escribir de forma recursiva."""
    pass # Completar


# NO MODIFICAR - INICIO
if __name__ == "__main__":
    assert numeros_al_final_recursivo([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN
