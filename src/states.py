import pygame
from .sprites import Santa
from .ui import Button

class State:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets

    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
        
    def draw(self, surface):
        pass


class MenuState(State):
    def __init__(self, game, assets):
        super().__init__(game, assets)
        self.santa = Santa(self.assets, 100, 300)
        

        sw = self.assets.images['sky'].get_width()

        tw = self.assets.images['title'].get_width()
        self.title_x = (sw / 2) - (tw / 2)
        self.title_y = self.assets.images['sky'].get_height() * 0.05

        btnw = self.assets.images['btn'].get_width()
        btns_x = (sw / 2) - (btnw / 2)
        btns_offset_y = 100
        first_btn_y = self.title_y+self.assets.images['title'].get_height() + btns_offset_y

        self.start_btn = Button(self.assets, btns_x, first_btn_y, "START ROUTE")
        self.settings_btn = Button(self.assets, btns_x, first_btn_y+btns_offset_y, "SETTINGS")
        self.exit_btn = Button(self.assets, btns_x, first_btn_y+btns_offset_y*2, "EXIT")

    def update(self, dt):
        self.santa.update(dt)
    
    def handle_event(self, event):
        if self.start_btn.handle_event(event):
            self.game.state = GameState(self.game, self.assets)
        elif self.settings_btn.handle_event(event):
            pass
        elif self.exit_btn.handle_event(event):
            return 1

    def draw(self, surface):
        surface.blit(self.assets.images['sky'], (0, 0))
        surface.blit(self.assets.images['menu_fg'], (0, 0))
        surface.blit(self.assets.images['title'], (self.title_x, self.title_y))
        
        surface.blit(self.santa.image, self.santa.rect)
        self.start_btn.draw(surface)
        self.settings_btn.draw(surface)
        self.exit_btn.draw(surface)

class GameState(State):
    def __init__(self, game, assets):
        super().__init__(game, assets)

    def handle_event(self, event):
        print(1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = MenuState(self.game, self.assets)
        
    def draw(self, surface):
        surface.blit(self.assets.images['sky'], (0, 0))
        surface.fill(pygame.Color(255, 255, 255, 50))