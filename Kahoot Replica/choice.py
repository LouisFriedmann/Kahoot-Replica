# choice.py contains a class so the user can make choices
import pygame

# Width and height of client's screen
WIDTH, HEIGHT = 800, 600

answer_choice_imgs = [pygame.image.load("images\\Answer Choices\\triangle.jpeg"),
                      pygame.image.load("images\\Answer Choices\\diamond.jpeg"),
                      pygame.image.load("images\\Answer Choices\\circle.jpeg"),
                      pygame.image.load("images\\Answer Choices\\square.jpeg")]

answer_choice_scaled_imgs = {"triangle": pygame.transform.scale(answer_choice_imgs[0], (WIDTH / 2, HEIGHT / 2)),
                             "diamond": pygame.transform.scale(answer_choice_imgs[1], (WIDTH / 2, HEIGHT / 2)),
                             "circle": pygame.transform.scale(answer_choice_imgs[2], (WIDTH / 2, HEIGHT / 2)),
                             "square": pygame.transform.scale(answer_choice_imgs[3], (WIDTH / 2, HEIGHT / 2))}
# Representing an answer choice that a user can click on
class Choice:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y

        self.width = answer_choice_scaled_imgs[shape].get_width()
        self.height = answer_choice_scaled_imgs[shape].get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.shape = shape

        self.clicked = False # Ensure that if button is held, button won't be continuously kicked

    def draw(self, win):
        img = answer_choice_scaled_imgs[self.shape]
        win.blit(img, (self.x, self.y))

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if not (pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos)):
            self.clicked = False

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos) and not self.clicked:
            self.clicked = True
            return True