import pygame
from src.settings import GAME_SIZE, FPS, CAPTION, MIN_SCREEN_SIZE
from src.loader import Assets
from src.states import MenuState

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(MIN_SCREEN_SIZE, pygame.RESIZABLE)

        self.assets = Assets()
        self.assets.load()

        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(self.assets.images['icon'])
        pygame.mouse.set_cursor(pygame.cursors.Cursor((0, 0), self.assets.images['cursor']))

        self.canvas = pygame.Surface(GAME_SIZE)
        self.state = MenuState(self, self.assets)
        self.clock = pygame.time.Clock()

    def run(self):
        dt = 0
        while True:
            canvas_to_screen_ratio = (self.canvas.get_width()/self.screen.get_width(), self.canvas.get_height()/self.screen.get_height())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    size = max(event.w, MIN_SCREEN_SIZE[0]), max(event.h, MIN_SCREEN_SIZE[1])
                    self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)

                # alter mouse related events to match the difference between canvas and actual window size
                if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    adj_x = event.pos[0] * canvas_to_screen_ratio[0]
                    adj_y = event.pos[1] * canvas_to_screen_ratio[1]
                    
                    event.pos = (adj_x, adj_y)

                if self.state.handle_event(event) == 1:
                    pygame.quit()
                    return

            self.state.update(dt)
            self.state.draw(self.canvas)

            # resize the canvas
            current_w, current_h = self.screen.get_size()
            scaled_canvas = pygame.transform.scale(self.canvas, (current_w, current_h))
            self.screen.blit(scaled_canvas, (0, 0))

            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000.0


if __name__ == "__main__":
    game = Game()
    game.run()
