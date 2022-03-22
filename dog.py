import pygame
from pygame.sprite import Sprite

class Dog(Sprite):
    """A class to represent a single dog in the pack."""

    def __init__(self, di_game):
        """Initialize the dog and set its starting position."""
        super().__init__()
        self.screen = di_game.screen
        self.settings = di_game.settings

        # Load the dog image and set its rect attribute.
        self.image = pygame.image.load('images/dog-running.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the dog's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if dog is at screen edge."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the dog right or left."""
        self.x += (self.settings.dog_speed * self.settings.pack_direction)
        self.rect.x = self.x


