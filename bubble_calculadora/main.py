from kivy.app import App
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.boxlayout import BoxLayout
import math

class calculaApp(App):
    bubble_shown = False  # Bandera para rastrear si el bubble está mostrado
    bubble = None  # Referencia al bubble actual

    def show_bubble(self, obj):
        if not self.bubble_shown:  # Si el bubble no está mostrado
            # Crear un nuevo bubble
            self.bubble = Bubble(orientation='horizontal',
                                 size_hint=(None, None),
                                 size=(160, 120),
                                 pos_hint={'center_x': .5, 'center_y': .5})
            box_layout = BoxLayout(orientation='horizontal', spacing=1)  # Layout para los botones

            # Función de manejo de eventos para el botón "SEN"
            def on_sen_press(instance):
                entry_value = self.root.ids.entry.text
                try:
                    number = float(entry_value)
                except ValueError:
                    self.root.ids.show.text = "Error: No es un número válido"
                    return

                # Calcular el seno del número
                result = math.sin(math.radians(number))
                formatted_result = f"{result:.4f}"
                self.root.ids.show.text = f"Sen({number}) = {formatted_result}"
                self.root.ids.show.cursor = (0, 0)

            # Crear y agregar botón "SEN" al bubble
            button_sen = BubbleButton(text="SEN", font_size = 30, size_hint_x=None, width=185, size_hint_y=None, height=100, background_color=(0, 2, 8, 3))
            button_sen.bind(on_press=on_sen_press)
            box_layout.add_widget(button_sen)

            # Función de manejo de eventos para el botón "COS"
            def on_cos_press(instance):
                entry_value = self.root.ids.entry.text
                try:
                    number = float(entry_value)
                except ValueError:
                    self.root.ids.show.text = "Error: No es un número válido"
                    return

                # Calcular el coseno del número
                result = math.cos(math.radians(number))
                formatted_result = f"{result:.4f}"
                self.root.ids.show.text = f"Cos({number}) = {formatted_result}"
                self.root.ids.show.cursor = (0, 0)

            # Crear y agregar botón "COS" al bubble
            button_cos = BubbleButton(text="COS", font_size = 30, size_hint_x=None, width=185, size_hint_y=None, height=100, background_color=(0, 2, 8, 3))
            button_cos.bind(on_press=on_cos_press)
            box_layout.add_widget(button_cos)

            # Agregar el layout de los botones al bubble
            self.bubble.add_widget(box_layout)

            # Agregar el bubble al layout principal
            self.root.add_widget(self.bubble)

            self.bubble_shown = True  # Actualizar el estado del bubble a mostrado
        else:  # Si el bubble está mostrado
            self.root.remove_widget(self.bubble)  # Remover el bubble del layout principal
            self.bubble = None  # Restablecer la referencia al bubble a None
            self.bubble_shown = False  # Actualizar el estado del bubble a no mostrado

if __name__ == '__main__':
    calculaApp().run()
