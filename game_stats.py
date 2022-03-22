from settings import Settings


class GameStats:
    """Track statistics for Dogs Invasion."""

    def __init__(self, di_game):
        """Initialize statistics."""
        self.settings = di_game.settings
        self.reset_stats()

        # Empezar juego en un estado inactivo.
        self.game_active = False


        # Start Dog Invasion in an active state.
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.players_left = self.settings.player_limit