from kivy.app import App
from kivy.uix.bubble import Bubble
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.lang import Builder

class CustomBubble(Bubble):
    visible = BooleanProperty(False) # Propiedad para controlar la visibilidad de bubble

    def on_visible(self, instance, value):
        self.opacity = 1 if value else 0
        self.disabled = not value

class RootWidget(FloatLayout):
    def toggle_bubble_visibility(self, bubble):
        bubble.visible = not bubble.visible # Cambiar la visibilidad de bubble

class ChatApp(App):
    def build(self):
        # Builder.load_file('bubble.kv')
        return RootWidget()

    def submit_message(self, text_input):
        print("Mensaje enviado:", text_input.text)
        text_input.text = ''  # Limpiar el cuadro de texto después de enviar

if __name__ == '__main__':
    Builder.load_file('bubble.kv')
    ChatApp().run() 