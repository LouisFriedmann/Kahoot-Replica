# main_board.py contains all information and behavior for the screen where players can see the questions,
# answer choices, and leaderboard
import math
import pygame
import random

from button import Button
from image import Image
from player import Player
from timer import Timer

# Width and height of main board's screen and main board FPS
MAIN_BOARD_WIDTH, MAIN_BOARD_HEIGHT = 1000, 750
FPS = 30

# Width and height of client's screen
CLIENT_WIDTH, CLIENT_HEIGHT = 800, 600

HORIZONTAL_SPACE_BETWEEN_NAMES = MAIN_BOARD_WIDTH / 16
VERTICAL_SPACE_BETWEEN_NAMES = MAIN_BOARD_HEIGHT / 5

VERTICAL_QUESTION_SPACE = MAIN_BOARD_HEIGHT / 100

START_BUTTON_WIDTH, START_BUTTON_HEIGHT = CLIENT_WIDTH / 10, CLIENT_HEIGHT / 8
SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT = CLIENT_WIDTH / 10, CLIENT_HEIGHT / 10

class MainBoard:
    def __init__(self, player_info_list, x, y, width, height, kahoot_name, questions, settings, random_names):
        self.player_info_list = player_info_list
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.kahoot_name = kahoot_name
        self.questions = questions
        self.num_questions = len(self.questions)
        self.settings = settings
        self.random_names = random_names

        # Buttons
        self.start_button = Button(x=self.width - START_BUTTON_WIDTH, y=0, width=START_BUTTON_WIDTH,
                                   height=START_BUTTON_HEIGHT, txt="Start", color="green")
        self.scroll_up_button = Button(x=0, y=VERTICAL_SPACE_BETWEEN_NAMES - SCROLL_BUTTON_HEIGHT, width=SCROLL_BUTTON_WIDTH,
                                       height=SCROLL_BUTTON_HEIGHT, txt="Up", color="grey")
        self.scroll_down_button = Button(x=self.scroll_up_button.width, y=VERTICAL_SPACE_BETWEEN_NAMES - SCROLL_BUTTON_HEIGHT,
                                         width=SCROLL_BUTTON_WIDTH,
                                         height=SCROLL_BUTTON_HEIGHT, txt="Down", color="grey")
        self.skip_button = Button(x=0, y=0, width=self.width / 10, height=self.height / 10, txt="Skip",
                                  color="grey")
        self.next_button = Button(x=0, y=0, width=self.width / 10, height=self.height / 10, txt="Next",
                                  color="blue")

        # Images
        shape_img_width, shape_img_height = self.width / 2, self.height / 6
        self.triangle_img = Image(self.x, self.height - shape_img_height * 2, shape_img_width, shape_img_height,
                                  img_key="server_triangle")
        self.diamond_img = Image(self.x + shape_img_width, self.height - shape_img_height * 2, shape_img_width,
                                 shape_img_height,
                                 img_key="server_diamond")
        self.circle_img = Image(self.x, self.height - shape_img_height, shape_img_width, shape_img_height,
                                img_key="server_circle")
        self.square_img = Image(self.x + shape_img_width, self.height - shape_img_height, shape_img_width,
                                shape_img_height,
                                img_key="server_square")
        self.checkbox_img = Image(0, 0, self.triangle_img.width / 8, self.triangle_img.height / 2,
                                  img_key="choices_checkbox")

        self.original_quiz_img_width, self.original_quiz_img_height = self.width / 6, self.width / 6
        self.quiz_img_x = self.x + self.width / 2 - self.original_quiz_img_width / 2  # Doesn't change
        # (quiz decoration, shaped like diamond, only goes up after each question)
        self.original_quiz_img_y = self.y + self.height / 2 - self.original_quiz_img_height / 2
        self.quiz_img = Image(self.quiz_img_x, self.original_quiz_img_y, self.original_quiz_img_width,
                              self.original_quiz_img_height, img_key="quiz_decoration")

        self.bar_width = self.width / 6 # width of each bar when answer choice distribution is shown, excluding the rectangle below white line
        self.shape_bar_height = self.height / 10 # height of each bar when answer choice distribution is shown, excluding the rectangle below white line

        self.space_choice_and_bar = self.height / 10
        total_bar_width = self.bar_width * 4
        start_x = self.x + self.width / 2 - total_bar_width / 2
        self.triangle_bar = Image(start_x, self.diamond_img.y - self.space_choice_and_bar - self.shape_bar_height,
                                  self.bar_width, self.shape_bar_height, img_key="server_triangle_bar")
        self.diamond_bar = Image(start_x + self.bar_width,
                                 self.diamond_img.y - self.space_choice_and_bar - self.shape_bar_height, self.bar_width,
                                 self.shape_bar_height, img_key="server_diamond_bar")
        self.circle_bar = Image(start_x + self.bar_width * 2,
                                self.diamond_img.y - self.space_choice_and_bar - self.shape_bar_height, self.bar_width,
                                self.shape_bar_height, img_key="server_circle_bar")
        self.square_bar = Image(start_x + self.bar_width * 3,
                                self.diamond_img.y - self.space_choice_and_bar - self.shape_bar_height, self.bar_width,
                                self.shape_bar_height, img_key="server_square_bar")
        self.bronze_medal_img = Image(0, 0, 0, 0, img_key="bronze_decoration")
        self.silver_medal_img = Image(0, 0, 0, 0, img_key="silver_decoration")
        self.gold_medal_img = Image(0, 0, 0, 0, img_key="gold_decoration")

        # When to change/update screens
        self.game_started = False
        self.handle_menu = True
        self.show_quiz_name = False
        self.is_quiz_img_done_moving = False
        self.show_countdown = False
        self.show_choices_screen = False
        self.display_correct_answer = False
        self.skip_question = False
        self.show_leaderboard = False
        self.show_results = False

        self.num_scrolls_up = 0 # For menu screen

        # Seconds for showing quiz name
        self.show_name_seconds_past = 0
        self.show_name_total_seconds = 5

        # More info about countdown screen
        self.countdown_seconds_past = 0
        self.quiz_staying_still_seconds = .5
        self.quiz_moving_seconds = .5
        self.countdown_total_seconds = 5 + self.quiz_staying_still_seconds + self.quiz_moving_seconds
        self.original_quiz_img_y = self.y + self.height / 2 - self.quiz_img.height / 2
        self.final_quiz_img_y = self.y + self.height / 4 - self.quiz_img.height / 2
        self.times_to_move_up = math.ceil(self.quiz_moving_seconds * FPS)
        self.handle_choices_seconds_past = 0

        # For each question, players' answers recorded here and reset each question
        self.num_answers = 0
        self.answer_distribution = {"triangle": 0, "diamond": 0, "circle": 0, "square": 0}

        self.question_idx = 0

        self.kahoot_phrases = ["Classroom perfection?", "Secret classroom superpowers?",
                               "Pure genius?", "Genius machine?"] # For client after they choose answer

        self.leaderboard = Leaderboard()

        self.players_answer_info = dict()
        self.player_menu_sound = False

        self.results_timer = Timer()

    def add_player_info(self, player_info):
        self.player_info_list.append(player_info)
        self.leaderboard.add(player_info)
        self.players_answer_info[player_info] = dict()

    def remove_player_info(self, player_info):
        if player_info in self.player_info_list:
            idx = self.player_info_list.index(player_info)
            self.player_info_list.remove(self.player_info_list[idx])
            self.leaderboard.remove(player_info)
            del self.players_answer_info[player_info]

    def handle_menu_screen(self, win, background):
        self.player_menu_sound = True
        win.fill(background)

        if len(self.player_info_list) == 0:
            font = pygame.font.SysFont(None, int(MAIN_BOARD_HEIGHT / 10))
            rendered_font = font.render(str("Waiting for players..."), True, "black")
            win.blit(rendered_font, (MAIN_BOARD_WIDTH / 2 - rendered_font.get_width() / 2,
                                     MAIN_BOARD_HEIGHT / 2 - rendered_font.get_height() / 2))

        # At the top, display: top left-number of players, middle- the word "kahoot", right- start button
        font = pygame.font.SysFont(None, int(MAIN_BOARD_HEIGHT / 10))
        rendered_num_players_font = font.render(f"Players: {len(self.player_info_list)}", True, "black")
        rendered_kahoot_font = font.render("Kahoot!", True, "black")
        win.blit(rendered_num_players_font, (0, 0))
        win.blit(rendered_kahoot_font, (MAIN_BOARD_WIDTH / 2 - rendered_kahoot_font.get_width() / 2, 0))

        # Draw all buttons
        self.scroll_up_button.draw(win)
        self.scroll_down_button.draw(win)
        self.start_button.draw(win)

        # Allow user to scroll if they click the scroll button and there are names off the screen in the particular direction
        if len(self.player_info_list) > 0:
            if self.scroll_up_button.is_clicked() and self.player_info_list[0].name_obj.y <= 0:
                self.num_scrolls_up += 1
            elif self.scroll_down_button.is_clicked() and self.player_info_list[-1].name_obj.y >= CLIENT_HEIGHT:
                self.num_scrolls_up -= 1

        pygame.draw.line(win, "black", (0, VERTICAL_SPACE_BETWEEN_NAMES), (MAIN_BOARD_WIDTH, VERTICAL_SPACE_BETWEEN_NAMES))
        # Draw all players' names centered on the screen
        next_row_of_players = []
        len_crnt_row = 0 # Sum of all players and spaces in the current row
        y = VERTICAL_SPACE_BETWEEN_NAMES * (self.num_scrolls_up + 1)
        for i, player in enumerate(self.player_info_list):
            # Compute the length of the current row based on the number of spaces between player names and each player name's width
            len_crnt_row += player.name_obj.width
            next_row_of_players.append(player)
            if len(next_row_of_players) > 1:
                len_crnt_row += HORIZONTAL_SPACE_BETWEEN_NAMES

            # Display the name on the center of the screen, making the ends of first and last name in
            # each row even with the edges of the board
            if len_crnt_row >= MAIN_BOARD_WIDTH:
                next_row_of_players = next_row_of_players[:-1]
                len_crnt_row -= (player.name_obj.width + HORIZONTAL_SPACE_BETWEEN_NAMES)
                x = (MAIN_BOARD_WIDTH - len_crnt_row) / 2
                for this_row_player in next_row_of_players:
                    if y == 0:
                        this_row_player.name_obj.update_position(x, y - this_row_player.name_obj.height)
                    else:
                        this_row_player.name_obj.update_position(x, y)

                    this_row_player.name_obj.draw(win)
                    x += (this_row_player.name_obj.width + HORIZONTAL_SPACE_BETWEEN_NAMES)
                next_row_of_players.clear()
                y += VERTICAL_SPACE_BETWEEN_NAMES
                next_row_of_players.append(player)
                len_crnt_row = player.name_obj.width

            if i == len(self.player_info_list) - 1:
                x = (MAIN_BOARD_WIDTH - len_crnt_row) / 2
                for this_row_player in next_row_of_players:
                    if y == 0:
                        this_row_player.name_obj.update_position(x, y - this_row_player.name_obj.height)
                    else:
                        this_row_player.name_obj.update_position(x, y)

                    this_row_player.name_obj.draw(win)
                    x += (this_row_player.name_obj.width + HORIZONTAL_SPACE_BETWEEN_NAMES)

            # Handle each player name obj's events when its kick and start buttons are clicked and when the name is clicked
            player.name_obj.handle_events()

            # Handle kicking players
            if player.name_obj.kick_me:
                self.remove_player_info(player)

        # When the user clicks the start button, start and lock the game and stop the menu screen music
        if self.start_button.is_clicked():
            self.game_started = True
            self.handle_menu = False
            self.show_quiz_name = True

    def handle_showing_quiz_name(self, win, background):
        win.fill(background)

        font = pygame.font.SysFont(None, int(self.height / 10))
        rendered_font = font.render(str(self.kahoot_name), True, "black")
        win.blit(rendered_font, (self.x + self.width / 2 - rendered_font.get_width() / 2, self.y))

        white_rect = pygame.draw.rect(win, "white",
                                      (self.x, self.y + rendered_font.get_height(), self.width, self.height / 20))
        pygame.draw.rect(win, "green", (self.x, self.y + rendered_font.get_height(), white_rect.width *
                                        (self.show_name_seconds_past / self.show_name_total_seconds),
                                        white_rect.height))

        rect_width, rect_height = self.width / 3, self.height / 3
        rect = pygame.draw.rect(win, "white", (self.x + self.width / 2 - rect_width / 2,
                                               self.y + self.height / 2 - rect_height / 2, rect_width, rect_height))
        font = pygame.font.SysFont(None, int(self.height / 10))
        rendered_font = font.render(f"{self.num_questions} questions", True, "black")
        win.blit(rendered_font, (rect.x + rect.width / 2 - rendered_font.get_width() / 2,
                                 rect.y + rect.height / 2 - rendered_font.get_height() / 2))
        self.show_name_seconds_past += 1 / FPS

        if self.show_name_seconds_past >= self.show_name_total_seconds:
            self.show_quiz_name = False
            self.show_countdown = True

    def handle_showing_countdown(self, win, background):
        win.fill(background)

        question_obj = self.questions[self.question_idx]

        font = pygame.font.SysFont(None, int(self.height / 10))
        rendered_question_font = font.render(f"Question {self.question_idx + 1} of {self.num_questions}",
                                    True, "black")
        win.blit(rendered_question_font, (self.x + self.width / 2 - rendered_question_font.get_width() / 2, self.y))
        blue_rect_width, blue_rect_height = self.width, self.height / 10
        pygame.draw.rect(win, "blue", (self.x, self.height - blue_rect_height, blue_rect_width,
                                       blue_rect_height))

        font = pygame.font.SysFont(None, int(self.height / 20))
        rendered_font = font.render(f"Win up to {question_obj.points} points!", True, "black")
        win.blit(rendered_font, (self.x + self.width / 2 - rendered_font.get_width() / 2,
                                 self.height - blue_rect_height / 2 - rendered_font.get_height() / 2))

        self.countdown_seconds_past += 1 / FPS

        # Move the quiz decoration up
        if self.quiz_staying_still_seconds <= self.countdown_seconds_past < self.quiz_staying_still_seconds + self.quiz_moving_seconds:
            self.quiz_img.set_pos(self.quiz_img.x, self.quiz_img.y - (
                        self.original_quiz_img_y - self.final_quiz_img_y) /self.times_to_move_up)

        elif self.quiz_staying_still_seconds + self.quiz_moving_seconds <= self.countdown_seconds_past < self.countdown_total_seconds:
            self.is_quiz_img_done_moving = True
            white_rect = pygame.draw.rect(win, "white",
                                          (self.x, self.y + rendered_question_font.get_height(), self.width, self.height / 20))
            pygame.draw.rect(win, "green", (self.x, self.y + rendered_question_font.get_height(), white_rect.width *
                                            ((self.countdown_seconds_past - self.quiz_moving_seconds - self.quiz_staying_still_seconds) / (self.countdown_total_seconds - self.quiz_moving_seconds - self.quiz_staying_still_seconds)),
                                            white_rect.height))

            self._handle_showing_question(win=win, question_obj=question_obj, start_y=self.y + self.height / 2)

        elif self.countdown_seconds_past >= self.countdown_total_seconds:
            self.show_countdown = False
            self.show_choices_screen = True
            self.is_quiz_img_done_moving = False
            self.countdown_seconds_past = 0

        self.quiz_img.draw(win)

    def _handle_showing_question(self, win, question_obj, start_y):
        font = pygame.font.SysFont(None, int(self.height / 12))
        word_list = question_obj.question.split(" ")
        next_row_str = ""
        rendered_row_font = None
        y = start_y
        for i, word in enumerate(word_list):
            next_row_str += word + " "
            rendered_row_font = font.render(next_row_str, True, "black")

            # Ensure the question doesn't go off the screen
            if rendered_row_font.get_width() > self.width:
                last_word = next_row_str.split(" ")[-2]
                next_row_str = next_row_str[:len(next_row_str) - len(last_word) - 1]
                rendered_row_font = font.render(next_row_str, True, "black")
                win.blit(rendered_row_font, (self.x + self.width / 2 - rendered_row_font.get_width() / 2,
                                             y))
                y += rendered_row_font.get_height() + VERTICAL_QUESTION_SPACE
                next_row_str = last_word + " "

            if i == len(word_list) - 1:
                win.blit(rendered_row_font, (self.x + self.width / 2 - rendered_row_font.get_width() / 2, y))

                # return the y position of the bottom of the question
                return y + rendered_row_font.get_height()

    def handle_choices(self, win, background):
        win.fill(background)

        question_obj = self.questions[self.question_idx]

        font = pygame.font.SysFont(None, int(self.height / 18))

        # Draw shapes at the bottom
        self.triangle_img.draw(win)
        rendered_font = font.render(str(question_obj.triangle), True, "white")
        win.blit(rendered_font, (self.triangle_img.x + self.triangle_img.width / 2 - rendered_font.get_width() / 2,
                                 self.triangle_img.y + self.triangle_img.height / 2 - rendered_font.get_height() / 2))

        self.diamond_img.draw(win)
        rendered_font = font.render(str(question_obj.diamond), True, "white")
        win.blit(rendered_font, (self.diamond_img.x + self.diamond_img.width / 2 - rendered_font.get_width() / 2,
                                 self.diamond_img.y + self.diamond_img.height / 2 - rendered_font.get_height() / 2))

        self.circle_img.draw(win)
        rendered_font = font.render(str(question_obj.circle), True, "white")
        win.blit(rendered_font, (self.circle_img.x + self.circle_img.width / 2 - rendered_font.get_width() / 2,
                                 self.circle_img.y + self.circle_img.height / 2 - rendered_font.get_height() / 2))

        self.square_img.draw(win)
        rendered_font = font.render(str(question_obj.square), True, "white")
        win.blit(rendered_font, (self.square_img.x + self.square_img.width / 2 - rendered_font.get_width() / 2,
                                 self.square_img.y + self.square_img.height / 2 - rendered_font.get_height() / 2))

        # Draw question at top of the screen
        line_y = self._handle_showing_question(win=win, question_obj=self.questions[self.question_idx], start_y=0)
        line = pygame.draw.line(win, "black", (0, line_y), (self.width, line_y))

        # Display right answer screen when the countdown hits zero or question is skipped and update the leaderboard
        if question_obj.seconds - self.handle_choices_seconds_past <= 0 or self.skip_question:
            self.leaderboard.update()
            self.display_correct_answer = True

        else:
            # Draw countdown circle middle-left
            radius = self.width / 10
            circle = pygame.draw.circle(win, "blue", (radius, self.height / 2), radius)
            font = pygame.font.SysFont(None, int(self.height / 10))
            rendered_font = font.render(str(int(question_obj.seconds - self.handle_choices_seconds_past)), True, "white")
            win.blit(rendered_font, (circle.x + circle.width / 2 - rendered_font.get_width() / 2,
                                     circle.y + circle.height / 2 - rendered_font.get_height() / 2))

            # Draw number of answers middle-right
            font = pygame.font.SysFont(None, int(self.height / 10))
            rendered_answer_font = font.render(f"{self.num_answers} answers", True, "black")
            answer_x, answer_y = self.width - rendered_answer_font.get_width(), self.y + self.height / 2 - rendered_answer_font.get_height() / 2
            win.blit(rendered_answer_font, (answer_x, answer_y))

            # Handle skip button
            self.skip_button.update_position(x=self.width - self.skip_button.width, y=line.y + self.next_button.height + self.width / 20)
            self.skip_button.draw(win)
            if self.skip_button.is_clicked():
                self.skip_question = True

            self.handle_choices_seconds_past += 1 / FPS

        # Display the checkbox within correct choice image
        if self.handle_choices_seconds_past >= question_obj.seconds or self.skip_question:
            if question_obj.correct_shape.lower() == "triangle":
                self.checkbox_img.set_pos(self.triangle_img.x + self.triangle_img.width - self.checkbox_img.width, self.triangle_img.y + self.triangle_img.height / 2 - self.checkbox_img.height / 2)
            elif question_obj.correct_shape.lower() == "diamond":
                self.checkbox_img.set_pos(self.diamond_img.x + self.diamond_img.width - self.checkbox_img.width, self.diamond_img.y + self.diamond_img.height / 2 - self.checkbox_img.height / 2)
            elif question_obj.correct_shape.lower() == "circle":
                self.checkbox_img.set_pos(self.circle_img.x + self.circle_img.width - self.checkbox_img.width, self.circle_img.y + self.circle_img.height / 2 - self.checkbox_img.height / 2)
            else:
                self.checkbox_img.set_pos(self.square_img.x + self.square_img.width - self.checkbox_img.width, self.square_img.y + self.square_img.height / 2 - self.checkbox_img.height / 2)

            self.checkbox_img.draw(win)

            # Handle next button
            rendered_answer_font = font.render(f"{self.num_answers} answers", True, "black")
            answer_y = self.y + self.height / 2 - rendered_answer_font.get_height() / 2
            self.next_button.update_position(x=self.width - self.next_button.width,
                                             y=line.y)
            self.next_button.draw(win)

            # Draw the answer choice distribution
            self.triangle_bar.draw(win)
            self.diamond_bar.draw(win)
            self.circle_bar.draw(win)
            self.square_bar.draw(win)

            number_font = pygame.font.SysFont(None, int(self.height / 10))
            total_bar_height = self.triangle_bar.y - line_y - number_font.get_height() # height of all four bars stacked on top of each other, excluding height of each shape bar (image)

            triangle_answers = self.answer_distribution["triangle"]
            diamond_answers = self.answer_distribution["diamond"]
            circle_answers = self.answer_distribution["circle"]
            square_answers = self.answer_distribution["square"]

            if self.num_answers == 0:
                triangle_percent = diamond_percent = circle_percent = square_percent = 0
            else:
                triangle_percent = triangle_answers / self.num_answers
                diamond_percent = diamond_answers / self.num_answers
                circle_percent = circle_answers / self.num_answers
                square_percent = square_answers / self.num_answers

            # draw each rectangle along with the number of answers for each
            rect = pygame.draw.rect(win, "red", (self.triangle_bar.x, self.triangle_bar.y - total_bar_height * triangle_percent, self.triangle_bar.width, total_bar_height * triangle_percent))
            rendered_font = font.render(str(triangle_answers), True, "red")
            win.blit(rendered_font, (self.triangle_bar.x + self.triangle_bar.width / 2 - rendered_font.get_width() / 2,
                                     self.triangle_bar.y - rect.height - rendered_font.get_height()))

            rect = pygame.draw.rect(win, "blue", (self.diamond_bar.x, self.diamond_bar.y - total_bar_height * diamond_percent, self.diamond_bar.width, total_bar_height * diamond_percent))
            rendered_font = font.render(str(diamond_answers), True, "blue")
            win.blit(rendered_font, (self.diamond_bar.x + self.diamond_bar.width / 2 - rendered_font.get_width() / 2,
                                     self.diamond_bar.y - rect.height - rendered_font.get_height()))

            rect = pygame.draw.rect(win, "orange", (self.circle_bar.x, self.circle_bar.y - total_bar_height * circle_percent, self.circle_bar.width, total_bar_height * circle_percent))
            rendered_font = font.render(str(circle_answers), True, "orange")
            win.blit(rendered_font, (self.circle_bar.x + self.circle_bar.width / 2 - rendered_font.get_width() / 2,
                                     self.circle_bar.y - rect.height - rendered_font.get_height()))

            rect = pygame.draw.rect(win, "darkgreen", (self.square_bar.x, self.square_bar.y - total_bar_height * square_percent, self.square_bar.width, total_bar_height * square_percent))
            rendered_font = font.render(str(square_answers), True, "darkgreen")
            win.blit(rendered_font, (self.square_bar.x + self.square_bar.width / 2 - rendered_font.get_width() / 2,
                                     self.square_bar.y - rect.height - rendered_font.get_height()))

            if self.next_button.is_clicked():
                self.display_correct_answer = False
                self.show_choices_screen = False
                self.show_leaderboard = True

    def handle_leaderboard(self, win, background):
        win.fill(background)

        font = pygame.font.SysFont(None, int(self.height / 5))
        rendered_leaderboard_font = font.render("Leaderboard", True, "black")
        win.blit(rendered_leaderboard_font, (self.x + self.width / 2 - rendered_leaderboard_font.get_width() / 2, self.y))

        self.next_button.update_position(self.x + self.width - self.next_button.width, self.y)
        self.next_button.draw(win)
        if self.next_button.is_clicked():
            self.next_question(win, background)

        top5 = self.leaderboard.get_top5() # List of lists, where each list is next place. Ex: [[name1, name2], name3]
        # name1 and name2 are in first, while name 3 is in third
        rect_width = self.width * (2 / 3)
        rect_x = self.x + self.width / 2 - rect_width / 2
        total_rect_height = self.height / 3
        player_rect_height = total_rect_height / 5
        y = self.y + self.height / 2 - total_rect_height / 2
        name_font = points_font = pygame.font.SysFont(None, int(self.height / 10))
        for i, player_list in enumerate(top5):
            for player in player_list:
                pygame.draw.line(win, "black", (rect_x, y + player_rect_height),
                                 (rect_x + rect_width, y + player_rect_height))
                if i == 0:
                   pygame.draw.rect(win, "white", (rect_x, y, rect_width, player_rect_height))

                rendered_name_font = name_font.render(player.name, True, "black")
                win.blit(rendered_name_font, (rect_x, y + player_rect_height / 2 - rendered_name_font.get_height() / 2))
                rendered_points_font = points_font.render(str(player.points), True, "black")
                win.blit(rendered_points_font, (rect_x + rect_width - rendered_points_font.get_width(),
                                                y + player_rect_height / 2 - rendered_name_font.get_height() / 2))
                y += player_rect_height

    def next_question(self, win, background):
        self._reset()
        self.show_leaderboard = False
        if self.question_idx == len(self.questions) - 1:
            self.show_results = True
            self.results_timer.start()
        else:
            self.question_idx += 1
            self.show_quiz_name = True

    # After each question, reset specific attributes of the class
    def _reset(self):
        self.quiz_img.set_pos(self.quiz_img_x, self.original_quiz_img_y)
        self.num_answers = 0
        self.answer_distribution["triangle"] = 0
        self.answer_distribution["diamond"] = 0
        self.answer_distribution["circle"] = 0
        self.answer_distribution["square"] = 0
        self.handle_choices_seconds_past = 0
        for player in self.players_answer_info.keys():
            self.players_answer_info[player].clear()
        self.skip_question = False

    def handle_results(self, win, background):
        win.fill(background)

        font = pygame.font.SysFont(None, int(self.height / 5))
        rendered_leaderboard_font = font.render("Podium", True, "gold")
        win.blit(rendered_leaderboard_font,
                 (self.x + self.width / 2 - rendered_leaderboard_font.get_width() / 2, self.y))

        space_between_rectangles = self.width / 20
        total_rect_horizontal_space = self.width * (3 / 4) + space_between_rectangles * 2
        vertical_distance_between_podiums = self.height / 7
        rect_width = (total_rect_horizontal_space - 2 * space_between_rectangles) / 3

        second_place_rect = pygame.draw.rect(win, "blue", (self.x + self.width / 2 - total_rect_horizontal_space / 2,
                                                                  self.height / 2 + vertical_distance_between_podiums,
                                                                  rect_width, self.height / 2 - vertical_distance_between_podiums))
        first_place_rect = pygame.draw.rect(win, "blue", (second_place_rect.x + rect_width + space_between_rectangles,
                                                                  self.height / 2,
                                                                  rect_width, self.height / 2))
        third_place_rect = pygame.draw.rect(win, "blue", (first_place_rect.x + rect_width + space_between_rectangles,
                                                                  self.height / 2 + vertical_distance_between_podiums * 2,
                                                                  rect_width, self.height / 2 - vertical_distance_between_podiums * 2))

        font = pygame.font.SysFont(None, int(self.height / 12))
        top3_players = self.leaderboard.get_top3_list()
        num_top_players = len(top3_players)
        third_show, second_show, first_show = 4, 8, 14 # The times that each place is shown best on the leaderboard music

        if num_top_players >= 2 and self.results_timer.elapsed_time() >= second_show:
            self.silver_medal_img.scale(second_place_rect.width / 3, second_place_rect.height / 3)
            self.silver_medal_img.set_pos(second_place_rect.x + second_place_rect.width / 2 - self.silver_medal_img.width / 2,
                                          second_place_rect.y + second_place_rect.height / 2 - self.silver_medal_img.height / 2)
            self.silver_medal_img.draw(win)

            rendered_second_place_font = font.render(top3_players[1].name, True, "black")
            win.blit(rendered_second_place_font, (second_place_rect.x + second_place_rect.width / 2 - rendered_second_place_font.get_width() / 2,
                                                  second_place_rect.y - rendered_second_place_font.get_height()))

        if self.results_timer.elapsed_time() >= first_show:
            self.gold_medal_img.scale(first_place_rect.width / 2, first_place_rect.height / 3)
            self.gold_medal_img.set_pos(first_place_rect.x + first_place_rect.width / 2 - self.gold_medal_img.width / 2,
                                          first_place_rect.y + first_place_rect.height / 2 - self.gold_medal_img.height / 2)
            self.gold_medal_img.draw(win)

            rendered_first_place_font = font.render(top3_players[0].name, True, "black")
            win.blit(rendered_first_place_font,
                     (first_place_rect.x + first_place_rect.width / 2 - rendered_first_place_font.get_width() / 2,
                      first_place_rect.y - rendered_first_place_font.get_height()))

        if num_top_players >= 3 and self.results_timer.elapsed_time() >= third_show:
            self.bronze_medal_img.scale(third_place_rect.width / 4, third_place_rect.height / 3)
            self.bronze_medal_img.set_pos(third_place_rect.x + third_place_rect.width / 2 - self.bronze_medal_img.width / 2,
                                          third_place_rect.y + third_place_rect.height / 2 - self.bronze_medal_img.height / 2)
            self.bronze_medal_img.draw(win)

            rendered_third_place_font = font.render(top3_players[2].name, True, "black")
            win.blit(rendered_third_place_font,
                     (third_place_rect.x + third_place_rect.width / 2 - rendered_third_place_font.get_width() / 2,
                      third_place_rect.y - rendered_third_place_font.get_height()))

    def handle_game(self, win, background):
        if self.show_quiz_name:
            self.handle_showing_quiz_name(win, background)

        if self.show_countdown:
            self.handle_showing_countdown(win, background)

        if self.show_choices_screen:
            self.handle_choices(win, background)

        if self.show_leaderboard:
            self.handle_leaderboard(win, background)

    def submit_answer(self, player, answer):
        player_info = self.player_info_list[self.player_info_list.index(player)]
        is_answer_correct = answer.lower() == self.get_correct_shape()
        self.players_answer_info[player_info]["is_answer_correct"] = is_answer_correct
        if is_answer_correct:
            total_points = self.questions[self.question_idx].points
            # This is for a spammer, spammer numbers are negative
            if player_info.num < 0:
                points = random.randint(1, total_points)

            # This is for a real player, player numbers are whole numbers
            else:
                points = total_points - (self.handle_choices_seconds_past / self.questions[self.question_idx].seconds) * total_points
            player_info.add_points(points)
            self.players_answer_info[player_info]["points"] = round(points)
        else:
            self.players_answer_info[player_info]["points"] = 0

        player_info.update_answer_streak(is_answer_correct=is_answer_correct)
        self.players_answer_info[player_info]["answer_streak"] = player_info.answer_streak
        self.num_answers += 1
        self.answer_distribution[answer] += 1

    def get_correct_shape(self):
        return self.questions[self.question_idx].correct_shape.lower()

    def get_answer_info(self, player):
        player_info = self.player_info_list[self.player_info_list.index(player)]

        # For the users who do not submit an answer
        if "answer_streak" not in self.players_answer_info[player_info]:
            self.players_answer_info[player_info]["is_answer_correct"] = False
            self.players_answer_info[player_info]["points"] = 0
            self.players_answer_info[player_info]["answer_streak"] = 0
            player_info.update_answer_streak(is_answer_correct=False)

        self.players_answer_info[player_info]["place"] = self.leaderboard.get_place(player_info)

        # Update other necessary info about a players' answer that couldn't be done until the countdown hit zero (ex: place on leaderboard)
        player_ahead = self.leaderboard.get_player_ahead(player_info)
        if player_ahead:
            self.players_answer_info[player_info]["player_ahead_name"] = player_ahead.name
            self.players_answer_info[player_info]["points_to_next_player"] = round(self.leaderboard.get_player_ahead(
                player_info).points - player_info.points)
        else:
            self.players_answer_info[player_info]["player_ahead_name"] = None
            self.players_answer_info[player_info]["points_to_next_player"] = None

        return self.players_answer_info[player_info]

# Storing all players' information
class PlayerInfo:
    def __init__(self, name, num, points):
        self.name = name
        self.num = num
        self.points = round(points)
        self.answer_streak = 0

        self.name_obj = PlayerName(self.name, self.num)

    def update_name(self, name):
        self.name = name

    def add_points(self, points):
        self.points += round(points)

    def update_answer_streak(self, is_answer_correct):
        print(self.answer_streak)
        if is_answer_correct:
            self.answer_streak += 1
        else:
            self.answer_streak = 0

# Representing player name on MainBoard
pygame.font.init()
name_font = pygame.font.SysFont(None, int(CLIENT_HEIGHT / 10))
class PlayerName:
    def __init__(self, name, num):
        self.name = name
        self.num = num

        self.x, self.y = 0, 0

        self.width = name_font.render(str(self.name), True, "black").get_width()
        self.height = name_font.render(str(self.name), True, "black").get_height()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.cancel_button = Button(x=self.x, y=self.y + self.height, width=self.width, height=self.height,
                                    txt="Cancel", color="green")
        self.kick_button = Button(x=self.x, y=self.y + self.height + self.cancel_button.height, width=self.width,
                                  height=self.height, txt="Kick", color="red")

        self.show_buttons = False
        self.kick_me = False

    def draw(self, win):
        rendered_font = name_font.render(str(self.name), True, "black")
        win.blit(rendered_font, (self.x, self.y))

        if self.show_buttons:
            self.cancel_button.draw(win)
            self.kick_button.draw(win)

        # Draw rectangle over the name if mouse is hovering over name
        if self.is_mouse_hovering():
            width_rect, height_rect = self.width, self.height / 4
            pygame.draw.rect(win, "black", (self.x, self.y + self.height / 2 - height_rect / 2,
                                            width_rect, height_rect))

    def handle_events(self):
        if self.is_clicked() and not self.show_buttons:
            self.show_buttons = True

        if self.show_buttons:
            if self.cancel_button.is_clicked():
                self.show_buttons = False

            elif self.kick_button.is_clicked():
                self.kick_me = True

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if not (pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos)):
            self.clicked = False

        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos) and not self.clicked:
            self.clicked = True
            return True

        return False

    # Returns True if mouse is hovering over name
    def is_mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)

    def update_name(self, name):
        self.name = name

        # Also width and height get updated accordingly based on the name
        self.width = name_font.render(str(self.name), True, "black").get_width()
        self.height = name_font.render(str(self.name), True, "black").get_height()

    def update_position(self, x, y):
        self.x = x
        self.y = y

        # Update the position of the rectangle and the buttons
        self.rect.x = x
        self.rect.y = y

        self.cancel_button.update_position(self.x, self.y + self.height)
        self.kick_button.update_position(self.x, self.y + self.height + self.cancel_button.height)

# Representing each question on MainBoard
class Question:
    def __init__(self, question, triangle, diamond, circle, square, correct_shape, points, seconds):
        self.question = question
        self.triangle = triangle
        self.diamond = diamond
        self.circle = circle
        self.square = square
        self.correct_shape = correct_shape
        self.points = points
        self.seconds = seconds

# Representing the settings on kahoot
class Settings:
    def __init__(self, is_random, is_spammer_enabled, is_music_enabled):
        self.is_random = is_random
        self.is_spammer_enabled = is_spammer_enabled
        self.is_music_enabled = is_music_enabled

# Representing the kahoot leaderboard
class Leaderboard:
    def __init__(self):
        self.points = []
        self.players = []
        self.leaderboard = []
        self.points_players = dict()

    def add(self, player_info):
        self.players.append(player_info)

    def remove(self, player_info):
        self.players.remove(player_info)
        self.update()

    def _update_players_points(self):
        self.points_players.clear()
        self.points.clear()
        for player_info in self.players:
            if player_info.points in self.points_players:
                self.points_players[player_info.points].append(player_info)
            else:
                self.points_players[player_info.points] = [player_info]
            self.points.append(player_info.points)

        self.points = sorted(self.points, reverse=True)

    def update(self):
        self._update_players_points()
        self.leaderboard.clear()
        prev = None
        i = 0
        for point_value in self.points:
            if point_value == prev:
                i += 1
                self.leaderboard[-1].append(self.points_players[point_value][i])
            else:
                i = 0
                self.leaderboard.append([self.points_players[point_value][i]])
            prev = point_value

    def get_place(self, player_info):
        place = 1
        for place_list in self.leaderboard:
            for next_player in place_list:
                if player_info == next_player:
                    return place
            place += len(place_list)


    def get_top5(self):
        players = 0
        player_list = []
        for place_list in self.leaderboard:
            player_list.append([])
            for next_player_info in place_list:
                player_list[-1].append(next_player_info)
                players += 1
                if players == 5:
                    return player_list

        return player_list

    def get_top3_list(self):
        top_5_list = []
        players_added = 0
        for place_list in self.leaderboard:
            for next_player_info in place_list:
                top_5_list.append(next_player_info)
                players_added += 1
                if players_added == 5:
                    return top_5_list

        return top_5_list


    def get_player_ahead(self, player_info):
        if self.get_place(player_info) == 1:
            return None

        for list_idx, next_list in enumerate(self.leaderboard):
            for player_info_obj in next_list:
                if player_info == player_info_obj:
                    return self.leaderboard[list_idx - 1][-1]