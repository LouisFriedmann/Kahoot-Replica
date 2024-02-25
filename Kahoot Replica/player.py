# player.py contains all information and behavior relative to a player
import pygame
import math
import random

from button import Button
from choice import Choice
from image import Image
from timer import Timer

# Width and height of client's screen
WIDTH, HEIGHT = 800, 600
TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT = WIDTH / 2, HEIGHT / 8
GO_BUTTON_WIDTH, GO_BUTTON_HEIGHT = WIDTH / 5, HEIGHT / 6

FPS = 30

# Representing each player that is playing kahoot
class Player:
    def __init__(self, screen_x, screen_y, screen_width, screen_height, num, name="", random_names=None):
        self.screen_x, self.screen_y = screen_x, screen_y
        self.screen_width, self.screen_height = screen_width, screen_height
        self.rect = pygame.Rect(self.screen_x, self.screen_y, self.screen_width, self.screen_height)

        self.num = num

        self.name = name
        self.random_names = random_names

        # For spinning for random name
        self.spin_button = Button(x=0, y=0, width=TEXT_BOX_WIDTH / 4, height=TEXT_BOX_HEIGHT, txt="Spin", color="green")
        self.spin_timer = Timer()
        self.spinning = False

        self.choices = [
            Choice(x=0, y=0, shape="triangle"),
            Choice(x=screen_width / 2, y=0, shape="diamond"),
            Choice(x=0, y=screen_height / 2, shape="circle"),
            Choice(x=screen_width / 2, y=screen_height / 2, shape="square")
        ]
        self.answer_chosen = None

        self.go_button = Button(x=self.screen_x + self.screen_width / 2 - GO_BUTTON_WIDTH / 2,
                                y=self.screen_y + self.screen_height * (3 / 4), width=GO_BUTTON_WIDTH, height=GO_BUTTON_HEIGHT,
                                txt="Go!", color="green")

        self.is_ready = False
        self.in_game = False
        self.joined_game = False
        self.display_nickname_screen = True
        self.display_waiting_to_start_screen = False
        self.display_answer_choices = False
        self.display_get_ready_screen = False
        self.display_is_answer_correct = False
        self.display_kahoot_phrase = False
        self.is_phrase_displaying = False
        self.answer_submitted = False

        self.countdown_seconds_past = 0

        self.colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        self.ready_crnt_color = random.choice(self.colors)
        self.ready_seconds_past = 0

        self.phrases_crnt_color = random.choice(self.colors)
        self.phrases_seconds_past = 0
        self.random_phrase = None

        self.checkbox_img = Image(0, 0, self.screen_width / 4, self.screen_height / 4, img_key="user_checkbox")
        self.x_img = Image(0, 0, self.screen_width / 4, self.screen_height / 4, img_key="user_x")

        self.got_answer_info = False
        self.answer_info = None

    def __eq__(self, other):
        return self.num == other.num

    def __hash__(self):
        return hash(self.num)

    # Draw the screen where the user will choose their nickname either randomly or their own custom name and
    # allow them to either draw a nickname randomly or they can make their own custom one and join the kahoot
    def handle_nickname_screen(self, win, pygame_events, is_random, background_color, is_kicked, random_names):
        win.fill(background_color)

        if is_kicked:
            word_to_display = "Rejoin Kahoot!"

        else:
            word_to_display = "Kahoot!"
        font = pygame.font.SysFont(None, int(TEXT_BOX_HEIGHT))
        rendered_font = font.render(word_to_display, True, "black")
        win.blit(rendered_font, (self.screen_x + self.screen_width / 2 - rendered_font.get_width() / 2,
                                 self.screen_y + self.screen_height / 4))

        # Draw the textbox
        text_box_x = self.screen_x + self.screen_width / 2 - TEXT_BOX_WIDTH / 2
        text_box_y = self.screen_x + self.screen_height / 2 - TEXT_BOX_HEIGHT / 2
        pygame.draw.rect(win, "white",
                         (text_box_x, text_box_y, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT))
        pygame.draw.lines(surface=win, color="black", closed=True,
                          points=[(text_box_x, text_box_y), (text_box_x + TEXT_BOX_WIDTH, text_box_y),
                                  (text_box_x + TEXT_BOX_WIDTH, text_box_y + TEXT_BOX_HEIGHT),
                                  (text_box_x, text_box_y + TEXT_BOX_HEIGHT)], width=2)

        # Spin the wheel for a random name if the host chose yes for "random kahoot generator"
        if is_random:
            self.spin_button.update_position(text_box_x + TEXT_BOX_WIDTH, text_box_y)
            self.spin_button.draw(win)
            if len(self.name) == 0:
                font = pygame.font.SysFont(None, int(TEXT_BOX_HEIGHT))
                rendered_font = font.render("Spin For Name", True, "grey")
                win.blit(rendered_font, (text_box_x + TEXT_BOX_WIDTH / 2 - rendered_font.get_width() / 2,
                                         text_box_y + TEXT_BOX_HEIGHT / 2 - rendered_font.get_height() / 2))

            if self.spin_button.is_clicked():
                self.spinning = True

            if self.spinning:
                spin_seconds = 3
                if self.spin_timer.elapsed_time() == 0:
                    self.spin_timer.start()

                elif self.spin_timer.elapsed_time() < spin_seconds:
                    self.name = random.choice(random_names)

                else:
                    self.spin_timer.reset()
                    self.spinning = False


        # Allow the user to type in the textbox
        else:
            if len(self.name) == 0:
                font = pygame.font.SysFont(None, int(TEXT_BOX_HEIGHT))
                rendered_font = font.render("Enter name", True, "grey")
                win.blit(rendered_font, (text_box_x + TEXT_BOX_WIDTH / 2 - rendered_font.get_width() / 2,
                                         text_box_y + TEXT_BOX_HEIGHT / 2 - rendered_font.get_height() / 2))

            for event in pygame_events:
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_BACKSPACE]:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode

                        # Ensure the width of the name doesn't exceed the textbox width
                        font = pygame.font.SysFont(None, int(TEXT_BOX_HEIGHT))
                        rendered_font = font.render(self.name, True, "black")
                        if rendered_font.get_width() > TEXT_BOX_WIDTH:
                            self.name = self.name[:-1]


        rendered_font = font.render(self.name, True, "black")
        win.blit(rendered_font, (text_box_x + TEXT_BOX_WIDTH / 2 - rendered_font.get_width() / 2,
                                 text_box_y + TEXT_BOX_HEIGHT / 2 - rendered_font.get_height() / 2))

        # Handle the go button
        self.go_button.draw(win)

        if self.go_button.is_clicked() and len(self.name) > 0 and not self.spinning:
            self.is_ready = True
            self.display_nickname_screen = False
            self.display_waiting_to_start_screen = True

    def handle_locked_screen(self, win, background_color):
        win.fill(background_color)

        font = pygame.font.SysFont(None, int(TEXT_BOX_HEIGHT))
        rendered_font = font.render("Game locked! Sorry.", True, "red")
        win.blit(rendered_font, (self.screen_x + self.screen_width / 2 - rendered_font.get_width() / 2,
                                 self.screen_y + self.screen_height / 2 - rendered_font.get_height() / 2))


    def handle_waiting_to_start_screen(self, win, background_color):
        win.fill(background_color)

        font = pygame.font.SysFont(None, int(HEIGHT / 10))
        rendered_font = font.render("Waiting for host to start...", True, "black")
        win.blit(rendered_font, (WIDTH / 2 - rendered_font.get_width() / 2, HEIGHT / 2 - rendered_font.get_height() / 2))

    def handle_get_ready_screen(self, win):
        if int(self.ready_seconds_past) > int(self.ready_seconds_past - 1 / FPS):
            # new_color_list excludes the current color so new color can be displayed each time
            new_color_list = self.colors[:self.colors.index(self.ready_crnt_color)] + (
                             self.colors[self.colors.index(self.ready_crnt_color) + 1:])
            self.ready_crnt_color = new_color_list[random.randint(0, len(new_color_list) - 1)]

        win.fill(self.ready_crnt_color)

        font = pygame.font.SysFont(None, int(HEIGHT / 5))
        get_ready_font = font.render("Get Ready!", True, "black")
        loading_font = font.render("Loading...", True, "black")
        total_height = get_ready_font.get_height() + loading_font.get_height() + HEIGHT / 20
        center_y = HEIGHT / 2

        win.blit(get_ready_font, (WIDTH / 2 - get_ready_font.get_width() / 2, center_y - total_height / 2))
        win.blit(loading_font, (WIDTH / 2 - loading_font.get_width() / 2, center_y + total_height / 2 - get_ready_font.get_height()))
        self.ready_seconds_past += 1 / FPS

    def handle_countdown_screen(self, win, background_color, countdown_seconds):
        win.fill(background_color)

        self.countdown_seconds_past += 1 / FPS

        font = pygame.font.SysFont(None, int(HEIGHT / 2))
        rendered_font = font.render(str(countdown_seconds - int(self.countdown_seconds_past)), True, "black")
        win.blit(rendered_font, (WIDTH / 2 - rendered_font.get_width() / 2, HEIGHT / 2 - rendered_font.get_height() / 2))

    # Draw the answer choices that the user can click on for each question and allow them to click one
    def handle_answer_choices(self, win):
        for choice in self.choices:
            choice.draw(win)

            if choice.is_clicked():
                self.answer_chosen = choice.shape

    def reset_answer(self):
        self.answer_chosen = None

    def handle_kahoot_phrase(self, win, phrases):
        if int(self.phrases_seconds_past) > int(self.phrases_seconds_past - 1 / FPS):
            # new_color_list excludes the current color so new color can be displayed each time
            new_color_list = self.colors[:self.colors.index(self.phrases_crnt_color)] + (
                self.colors[self.colors.index(self.phrases_crnt_color) + 1:])
            self.phrases_crnt_color = new_color_list[random.randint(0, len(new_color_list) - 1)]

        win.fill(self.phrases_crnt_color)

        font = pygame.font.SysFont(None, int(self.screen_height / 8))
        if not self.is_phrase_displaying:
            self.random_phrase = random.choice(phrases)
            self.is_phrase_displaying = True

        rendered_font = font.render(str(self.random_phrase), True, "white")
        win.blit(rendered_font, (self.screen_x + self.screen_width / 2 - rendered_font.get_width() / 2,
                                 self.screen_y + self.screen_height / 2 - rendered_font.get_height() / 2))
        self.phrases_seconds_past += 1 / FPS

    def handle_is_answer_correct(self, win, answer_info):
        font = pygame.font.SysFont(None, int(self.screen_height / 10))

        if answer_info:
            answer_streak_font = font.render(f"Answer streak: {answer_info['answer_streak']}", True, "black")
            points_font = font.render(f"+{answer_info['points']}", True, "black")
            points_rect_width, points_rect_height = self.screen_width / 3, self.screen_height / 10
            y = None
            rect_color = None
            if answer_info["is_answer_correct"]:
                win.fill("green")
                correct_font = font.render("Correct", True, "black")
                middle_rect_height = correct_font.get_height() + answer_streak_font.get_height() + \
                                     points_rect_height # For checkbox, answer streak, and points earned combined
                y = self.screen_y + self.screen_height / 2 - middle_rect_height
                win.blit(correct_font, (self.screen_x + self.screen_width / 2 - correct_font.get_width() / 2, y))
                y += correct_font.get_height()
                self.checkbox_img.set_pos(self.screen_x + self.screen_width / 2 - self.checkbox_img.width / 2, y)
                y += self.checkbox_img.height
                self.checkbox_img.draw(win)
                rect_color = "darkgreen"

            else:
                win.fill("red")
                font2 = pygame.font.SysFont(None, int(self.screen_height / 10))
                incorrect_font = font2.render("Incorrect", True, "black")
                middle_rect_height = incorrect_font.get_height() + answer_streak_font.get_height() + \
                                     points_rect_height  # For checkbox, answer streak, and points earned combined  # For "x", answer streak, and points earned combined
                y = self.screen_y + self.screen_height / 2 - middle_rect_height
                win.blit(incorrect_font, (self.screen_x + self.screen_width / 2 - incorrect_font.get_width() / 2, y))
                y += incorrect_font.get_height()
                self.x_img.set_pos(self.screen_x + self.screen_width / 2 - self.checkbox_img.width / 2, y)
                y += self.x_img.height
                self.x_img.draw(win)
                rect_color = "darkred"

            win.blit(answer_streak_font, (self.screen_x + self.screen_width / 2 - answer_streak_font.get_width() / 2, y))
            y += answer_streak_font.get_height()
            points_rect = pygame.draw.rect(win, rect_color, (self.screen_x + self.screen_width / 2 - points_rect_width / 2,
                                                              y, points_rect_width, points_rect_height))
            win.blit(points_font, (points_rect.x + points_rect.width / 2 - points_font.get_width() / 2,
                                   points_rect.y + points_rect.height / 2 - points_font.get_height() / 2))

            font = pygame.font.SysFont(None, int(self.screen_height / 20))
            if answer_info["place"] == 1:
                rendered_place_font = font.render(f"Place: 1", True, "black")
            else:
                rendered_place_font = font.render(f"Place: {answer_info['place']}, {answer_info['points_to_next_player']} points behind {answer_info['player_ahead_name']}", True, "black")
            win.blit(rendered_place_font, (self.screen_x + self.screen_width / 2 - rendered_place_font.get_width() / 2,
                                           self.screen_y + self.screen_height * (5 / 6) - rendered_place_font.get_height() / 2))

    # Reset certain attributes of player after each question
    def reset(self):
        self.countdown_seconds_past = 0
        self.answer_chosen = None
        self.display_is_answer_correct = False
        self.answer_submitted = False
        self.got_answer_info = False