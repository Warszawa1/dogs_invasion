import pygame


class Player:
    """A class to manage the ship."""

    def __init__(self, di_game):
        """Initialize the player and set its starting position."""
        self.screen = di_game.screen
        self.screen_rect = di_game.screen.get_rect()
        self.settings = di_game.settings

        # Load the player image and get its rect.
        self.image = pygame.image.load('images/player.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the player's position based on the movement flag."""
        # Update the player's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.player_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.player_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_player(self):
        """Center the player on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

