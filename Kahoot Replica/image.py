# image.py contains a class used to represent images in kahoot

import pygame

# Representing an image to be used in kahoot
loaded_imgs = {"quiz_decoration": pygame.image.load("images\\Decorations\\quiz_decoration.png"),
               "server_triangle": pygame.image.load("images\\server answer choices\\triangle.png"),
               "server_diamond": pygame.image.load("images\\server answer choices\\diamond.png"),
               "server_circle": pygame.image.load("images\\server answer choices\\circle.png"),
               "server_square": pygame.image.load("images\\server answer choices\\square.png"),
               "server_triangle_bar": pygame.image.load("images\\server answer choices\\triangle.png"),
               "server_diamond_bar": pygame.image.load("images\\server answer choices\\diamond.png"),
               "server_circle_bar": pygame.image.load("images\\server answer choices\\circle.png"),
               "server_square_bar": pygame.image.load("images\\server answer choices\\square.png"),
               "choices_checkbox": pygame.image.load("images\\other\\checkbox.png"),
               "user_checkbox": pygame.image.load("images\\other\\checkbox.png"),
               "user_x": pygame.image.load("images\\other\\x_image.png"),
               "bronze_decoration": pygame.image.load("images\\other\\bronze.png"),
               "silver_decoration": pygame.image.load("images\\other\\silver.png"),
               "gold_decoration": pygame.image.load("images\\other\\gold.png")

              }

class Image:
    def __init__(self, x, y, width, height, img_key):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.img_key = img_key

    def draw(self, win):
        scaled_img = pygame.transform.scale(loaded_imgs[self.img_key], (self.width, self.height))
        win.blit(scaled_img, (self.x, self.y))

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def scale(self, width, height):
        self.width, self.height = width, height