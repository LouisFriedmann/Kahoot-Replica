# button.py represents buttons users or the host can press during the game
import pygame

# Width and height of client's screen
WIDTH, HEIGHT = 800, 600

# Representing a button a user can click on
class Button:
    def __init__(self, x, y, width, height, txt, color):
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.txt = txt
        self.color = color

        self.clicked = False # Ensure that if button is held, button won't be continuously kicked

    # Draw the rectangle and the centered text
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.lines(surface=win, color="black", closed=True,
                          points=[(self.x, self.y), (self.x + self.width, self.y),
                                  (self.x + self.width, self.y + self.height),
                                  (self.x, self.y + self.height)], width=2)

        font = pygame.font.SysFont(None, int(self.height / 2))
        rendered_font = font.render(str(self.txt), True, "white")
        win.blit(rendered_font, (self.x + self.width / 2 - rendered_font.get_width() / 2,
                                 self.y + self.height / 2 - rendered_font.get_height() / 2))

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if not (pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos)):
            self.clicked = False

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos) and not self.clicked:
            self.clicked = True
            return True

    def update_position(self, x, y):
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y