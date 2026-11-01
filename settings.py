class Settings:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (35,35,35)
        self.ship_speed = 5
        self.speedup_scale =1.1
        self.initialize_dynamic_settings()

        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0,0,255)
        self.bullets_allowed = 25

        self.alien_speed = 3
        self.fleet_drop_speed = 8
        self.fleet_direction = 1 
        
        self.ship_limit = 0
        self.alien_points = 10

    def initialize_dynamic_settings(self):
        self.ship_speed = 3
        self.bullet_speed = 3.0
        self.alien_speed = 2.0
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
