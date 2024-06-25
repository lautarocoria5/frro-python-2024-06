from kivy.app import App
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

class CustomBubble(Bubble):
    def __init__(self, text_input, **kwargs):
        super().__init__(**kwargs)
        self.text_input = text_input
        for opc in [':D', ':|', ':(']:
            btn = BubbleButton(text=opc)
            btn.bind(on_release=self.on_option_select)
            self.ids.bubble_layout.add_widget(btn)

    def on_option_select(self, button):
        self.text_input.text += button.text
        # Ocultar la burbuja cuando se selecciona una opción
        self.parent.remove_widget(self)

class RootWidget(FloatLayout):
    pass

class ChatApp(App):
    def build(self):
        Builder.load_file('bubble.kv')
        return RootWidget()

    def show_bubble(self, button, text_input):
        # Agregar nueva burbuja sobre el botón "Emojis"
        bubble = CustomBubble(text_input)
        bubble.pos = (button.x, button.y + button.height)
        # Acceder al id float_layout directamente desde la instancia RootWidget
        self.root.float_layout.add_widget(bubble)

    def submit_message(self, text_input):
        print("Mensaje enviado:", text_input.text)
        text_input.text = ''  # Limpiar el cuadro de texto después de enviar

if __name__ == '__main__':
    ChatApp().run()