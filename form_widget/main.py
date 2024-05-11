from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
import re

class Pantalla1(Screen):
    def update_progress_bar(self):
        total_inputs = 4  # Número total de TextInput
        filled_inputs = sum(1 for child in self.ids.values() if isinstance(child, TextInput) and child.text)
        progress_value = filled_inputs / total_inputs if total_inputs > 0 else 0
        self.ids.pb.value = progress_value

    def validate_email(self, email):
        # Expresión regular para validar el formato de correo electrónico
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            print("Correo electrónico válido:", email)
        else:
            print("Correo electrónico inválido:", email)


class Pantalla2(Screen):
    pass


class formApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Pantalla1(name="pantalla1"))
        sm.add_widget(Pantalla2(name="pantalla2"))
        return sm


if __name__ == '__main__':
    formApp().run()