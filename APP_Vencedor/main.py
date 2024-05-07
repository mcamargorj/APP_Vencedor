from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from random import randint

class RoundedImage(Image):
    def __init__(self, **kwargs):
        super(RoundedImage, self).__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = False
        self.border_radius = [20,]

class ResetButton(Button):
    def __init__(self, **kwargs):
        super(ResetButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.6, 0.8, 1)  # Cor de fundo do botão (azul claro)
        self.border_radius = 30  # Raio dos cantos do botão
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'right': 0.95, 'top': 0.95}  # Posição do botão no canto superior direito

class VencedorApp(App):
    def build(self):
        layout = FloatLayout()
        
        # Adicionando um fundo estilo "gamer"
        background = Image(source='assets/background.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Imagem padrão com cantos arredondados
        self.resultado_sorteio = RoundedImage(source='assets/inicio.png', size_hint=(None, None), size=(300, 300),
                                               pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(self.resultado_sorteio)

        botao = Button(text="Sortear", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05})
        botao.bind(on_press=self.animar_imagem)  
        layout.add_widget(botao)

        self.label_vencedor = Label(text="O vencedor de hoje é...", size_hint=(None, None), size=(400, 50),
                                     pos_hint={'center_x': 0.5, 'y': 0.35}, font_size='24sp', color=(1, 1, 1, 1))
        self.label_vencedor.opacity = 0
        layout.add_widget(self.label_vencedor)

        reset_button = ResetButton(text="Reset")  # Criação do botão de reset
        reset_button.bind(on_press=self.reset_app)  # Associa a função reset_app ao evento de pressionar o botão
        layout.add_widget(reset_button)  # Adiciona o botão de reset ao layout

        # Carrega o som de vencedor
        self.sound = SoundLoader.load('assets/winner.wav')

        return layout

    def animar_imagem(self, instance):
        # Define a imagem padrão novamente antes do sorteio
        self.resultado_sorteio.source = 'assets/inicio.png'

        # Gera um número aleatório entre 1 e 6 (índices das imagens)
        vencedor = randint(1, 6)
        # Define a imagem correspondente ao resultado do dado
        nova_imagem = 'assets/'+f'foto{vencedor}.png'
        
        # Cancela qualquer animação anterior
        Animation.cancel_all(self.resultado_sorteio)

        # Define e inicia a animação de aumento de tamanho
        anim = Animation(size=(400, 400), duration=0.8)
        anim.bind(on_complete=lambda *args: self.set_new_image(nova_imagem)) 
        anim.start(self.resultado_sorteio)

        # Reproduz o som de vencedor
        if self.sound:
            self.sound.play()

    def set_new_image(self, nova_imagem, *args):
        # Define a nova imagem após a animação de aumento de tamanho
        self.resultado_sorteio.source = nova_imagem

        # Exibe a mensagem "O vencedor de hoje é"
        self.label_vencedor.opacity = 1

        # Define e inicia a animação de redução de tamanho
        anim = Animation(size=(300, 300), duration=0.8)
        anim.start(self.resultado_sorteio)

    def reset_app(self, instance):
        # Define a imagem padrão novamente ao pressionar o botão de reset
        self.resultado_sorteio.source = 'assets/inicio.png'
        self.label_vencedor.opacity = 0  # Oculta a mensagem de vencedor

if __name__ == '__main__':
    VencedorApp().run()
