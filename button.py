import pygame.font


class Button:

    def __init__(self, di_game, msg):
        """Inicializar los atributos del botón"""
        self.screen = di_game.screen
        self.screen_rect = self.screen.get_rect()

        # Configurar el tamanyo y las propiedades del botón.
        self.width, self.height = 200, 50
        self.button_color = (2, 14, 12)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Construir el objeto rect del botón y centrarlo.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # El mensaje del botón tiene que prepararse sólo una vez.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Transformar msg en una imagen renderizada y centrar el texto del botón."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Dibujar un botón en blanco y luego dibujar el mensaje.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)