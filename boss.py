import pygame
from pygame.sprite import Sprite


class Boss(Sprite):
    def __init__(self, ai_game):
        super().__init__()        
        self.screen = ai_game.screen 
        self.settings = ai_game.settings

        original_image = pygame.image.load("images/boss.png")
        self.image = pygame.transform.scale(original_image, (180,180))
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.top = 20

        self.hp = 10 
        self.direction = 1
        self.speed = 3.0
        self.x =  float(self.rect.x)

    def update(self):
        self.x += (self.speed * self.direction)
        self.rect.x = self.x
        
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            self.direction *= -1  

    def draw_health_bar(self):
        bar_width = self.rect.width
        bar_height = 10

        bg_rect = pygame.Rect(self.rect.x ,self.rect.top -10 , bar_width , bar_height)
        pygame.draw.rect(self.screen , (255,0,0), bg_rect)

        hp_ratio = self.hp / 10.0
        hp_width = int(bar_width * hp_ratio)

        if self.hp > 0 :
            hp_rect = pygame.Rect (self.rect.x ,self.rect.top -20 , hp_width , bar_height)
            pygame.draw.rect(self.screen , (0,255,0), hp_rect)


        