import sys
from time import sleep 
import pygame 
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard 
from pathlib import Path
from boss import Boss 


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()


        self.screen = pygame.display.set_mode((0,0) , pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.bg_image = pygame.image.load('images/background.jpg')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))


        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False

        self.play_button = Button(self, "Play")
        self.shoot_sound = pygame.mixer.Sound("sounds/shot.mp3")     




    def run_game(self):
        while True:
            self.check_event()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.bosses.update()
        
            self._update_screen()
            self.clock.tick(60)


    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)
        print(len(self.bullets))
        self._check_bullet_alien_collisions()



    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True , True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb._check_high_score()

        boss_collisions = pygame.sprite.groupcollide(
            self.bullets , self.bosses , True , False)
        
        if boss_collisions:
            for bosses_hit in boss_collisions.values():
                for boss in bosses_hit:
                    boss.hp -= 1
                    if boss.hp <= 0:
                        boss.kill()
                        self.stats.score += 1000
                        self.sb.prep_score()
                        self.sb._check_high_score()

        if not self.aliens and not self.bosses:
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level +=1
            self.sb.prep_level()

            if self.stats.level %3 == 0 :
                self._create_boss()
            else:
                self._create_fleet()

            self.sb._check_high_score() 


            

            
    
        

    def check_event(self):   
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _close_game(self):
        path = Path("high_score.txt")
        path.write_text(str(self.stats.high_score))

        pygame.quit()
        sys.exit()

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True

            self.sb.prep_score()
            self.sb.prep_level()

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()


            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
             
        if event.key == pygame.K_RIGHT:  
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key ==pygame.K_q:
            self._close_game()

       

    def _check_keyup_events(self,event):
      
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
                
        if event.key == pygame.K_LEFT:
            self.ship.moving_left  = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            self.shoot_sound.play()


    def _update_screen(self):
        self.screen.blit(self.bg_image, (0, 0))
        for bullet in self.bullets.sprites():bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.bosses.draw(self.screen)

        for boss in self.bosses.sprites():
            boss.draw_health_bar()

        if not self.game_active:
            self.play_button.draw_button()

        self.sb.show_score() 
        pygame.display.flip()
       
        

    def _create_fleet(self):
        alien = Alien(self)
        
        alien_width , alien_height = alien.rect.size 
        current_x , current_y = alien_width , alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):

            current_x = alien_width 
            while current_x < (self.settings.screen_width - 2 *alien_width ) :
                self._create_alien(current_x,current_y)

          
                current_x += 2* alien_width 
            current_y += 2 * alien_height

    def _create_boss(self):
        boss = Boss(self)
        self.bosses.add(boss)

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()

        if pygame.sprite.spritecollideany(self.ship , self.aliens ):
            print("Ship Hit !!")
            self._ship_hit()
        
        

        
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
   
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False

            pygame.mouse.set_visible(True) 

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


   

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()