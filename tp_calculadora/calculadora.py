from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
import ast # Evaluar resultado de operaciones, evitando errores de sintaxis 

# Tamaño de la ventana por defecto
Window.size = (500, 700)

class Calculadora(Widget):

    # Limpia el TextInput (AC)
    def limpiar_pantalla(self):
        self.ids.input.text = '0'

    def presionar_boton(self, button):
        input_actual = self.ids.input.text
        if 'Error' in input_actual:
            input_actual = ""
        # Si TextInput es '0', lo limpia antes de agregar nuevos caracteres
        if input_actual == '0': 
            self.ids.input.text = ''
        self.ids.input.text += button

    def cambiar_signo(self): # +/-
        input_actual = self.ids.input.text
        if input_actual.startswith('-'):
            self.ids.input.text = input_actual[1:]
        else:
            self.ids.input.text = '-' + input_actual
    
    def eliminar_ultimo(self): # DEL
        input_actual = self.ids.input.text
        if len(input_actual) == 1:
            self.ids.input.text = '0' # Si hay un solo caracter, imprime '0'
        elif input_actual:
            self.ids.input.text = input_actual[:-1]
    
    def punto_decimal(self):
        input_actual = self.ids.input.text
        # Evita problemas de sintaxis al introducir '.' donde no va
        if not input_actual or input_actual.endswith(('+', '-', '*', '/')) or '.' in input_actual.split()[-1]:
            return
        self.ids.input.text += '.'
    
    def operador_matematico(self, sign):
        input_actual = self.ids.input.text
        # Evita problemas de sintaxis al introducir operadores donde no va
        if input_actual and input_actual[-1] not in ('+', '-', '*', '/', '%'):
            self.ids.input.text += sign

    def calcular(self):
        input_actual = self.ids.input.text
        try:
            node = ast.parse(input_actual, mode='eval')
            resultado = eval(compile(node, '', 'eval'))
            self.ids.input.text = str(resultado)
        # Manejo de errores
        except ZeroDivisionError:
            self.ids.input.text = 'Error: División entre cero'
        except SyntaxError:
            self.ids.input.text = 'Error: Sintaxis incorrecta'
        except Exception as e:
            self.ids.input.text = f'Error: {e}'

class CalculadoraApp(App):
    def build(self):
        return Calculadora()

if __name__ == '__main__':
    CalculadoraApp().run()
