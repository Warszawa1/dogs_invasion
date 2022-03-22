class Settings:
    """A class to store all settings for Dogs Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 900
        self.screen_height = 1000
        self.bg_color = (230, 230, 230)

        # Player settings
        self.player_speed = 1.5
        self.player_limit = 3

        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 5
        self.bullet_height = 8
        self.bullet_color = (239, 0, 0)
        self.bullets_allowed = 30

        # Dog settings
        self.dog_speed = 2.0
        self.pack_drop_speed = 10
        # Pack_direction of 1 represents right; -1 represents left.
        self.pack_direction = 1



