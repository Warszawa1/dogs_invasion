import pygame
import sys
from time import sleep

from settings import Settings
from game_stats import GameStats
from player import Player
from bullet import Bullet
from dog import Dog
from button import Button

clock = pygame.time.Clock()
game_on = True


class DogsInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.settings = Settings()
        # Full screen mode
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("🐶🐾 Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.player = Player(self)
        self.bullets = pygame.sprite.Group()
        self.dogs = pygame.sprite.Group()

        self._create_pack()

        # Crear el botón de play.
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Start the main loop for the game."""
        while game_on:
            self._check_events()

            if self.stats.game_active:
                self.player.update()
                self._update_bullets()
                self._update_dogs()
            self._update_screen()

    # Watch for keyboard and mouse events.
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Empezar un juego nuevo cuando el jugador pulsa Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Hacer desaparecer el cursor del ratón.
            pygame.mouse.set_visible(False)

            # Resetea las estadísticas del juego.
            self.stats.reset_stats()
            self.stats.game_active = True



            # Desechar los perros y las pelotas restantes.
            self.dogs.empty()
            self.bullets.empty()

            # Crear un nuevo pack y centrar el jugador.
            self._create_pack()
            self.player.center_player()

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Check for any bullets that have hit dogs.
        # If so, get rid of the bullet and the alien.

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_dog_collisions()

    def _check_bullet_dog_collisions(self):
        """Respond to bullet-dog collisions"""
        # Remove any bullets and dogs that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.dogs, True, True)
        # Update bullet positions.
        self.bullets.update()
        if not self.dogs:
            # Destroy existing bullets and create new pack.
            self.bullets.empty()
            self._create_pack()

    def _create_pack(self):
        """Create the pack of dogs."""
        # Create the pack of dogs.
        # Spacing between each dog is equal to one dog width.
        dog = Dog(self)
        dog_width, dog_height = dog.rect.size
        available_space_x = self.settings.screen_width - (2 * dog_width)
        number_dogs_x = available_space_x // (2 * dog_width)

        # Determine the number of rows of dogs that fit on the screen.
        player_height = self.player.rect.height
        available_space_y = (self.settings.screen_height - (3 * dog_height) - (11 * player_height))
        number_rows = available_space_y // (2 * dog_height)

        # Create the full pack of dogs.
        for row_number in range(number_rows):
            for dog_number in range(number_dogs_x):
                self._create_dog(dog_number, row_number)

    def _create_dog(self, dog_number, row_number):
        """Create a dog and place it in the row."""
        dog = Dog(self)
        dog_width, dog_height = dog.rect.size
        dog.x = dog_width + 2 * dog_width * dog_number
        dog.rect.x = dog.x
        dog.rect.y = dog.rect.height + 2 * dog.rect.height * row_number
        self.dogs.add(dog)

    def _check_pack_edges(self):
        """Respond appropriately if any dogs have reached an edge."""
        for dog in self.dogs.sprites():
            if dog.check_edges():
                self._change_pack_direction()
                break

    def _change_pack_direction(self):
        """Drop the entire pack and change the pack's direction."""
        for dog in self.dogs.sprites():
            dog.rect.y += self.settings.pack_drop_speed
        self.settings.pack_direction *= -1

    def _update_dogs(self):
        """Check if the pack is at an edge, then update the positions of all dogs in the pack."""
        self._check_pack_edges()
        self.dogs.update()

        # Look for dog-player collisions.
        if pygame.sprite.spritecollideany(self.player, self.dogs):
            self._player_hit()

    def _player_hit(self):
        """Respond to the player being hit by a dog."""
        if self.stats.players_left > 0:
            # Decrement players_left.
            self.stats.players_left -= 1
            print(self.stats.players_left)

            # Get rid of any remaining dogs and bullets.
            self.dogs.empty()
            self.bullets.empty()

            # Create a new pack and center the player.
            self._create_pack()
            self.player.center_player()



            # Pause.
            sleep(0.5)
        elif self.stats.players_left == 0:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            print("GAME OVER!!")

    def _check_dogs_bottom(self):
        """Check if any dogs have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for dog in self.dogs.sprites():
            if dog.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the player got hit.
                self._player_hit()
                break

    # Redraw the screen during each pass through the loop.
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.dogs.draw(self.screen)

        # Dibujar el botón si el juego está inactivo.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Hacer la pantalla dibujada más reciente visible.
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    di = DogsInvasion()
    di.run_game()

