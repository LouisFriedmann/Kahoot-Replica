# server.py connects users to the server used by the kahoot replica

import socket
import _thread
import pickle
import pygame
import os
import random
import time

from player import Player

from main_board import MainBoard, PlayerInfo
from handle_csv import handle_csv_file
from kahoot_smasher import KahootSmasher
from sound_handler import SoundHandler

PORT = 5050
BYTES_TO_RECEIVE = 8192*8

CLIENT_WIDTH, CLIENT_HEIGHT = 800, 600

MAIN_BOARD_WIDTH, MAIN_BOARD_HEIGHT = 1000, 750

FPS = 30

players = dict()

def threaded_player(conn, player_num):
    data = {"player": players[player_num], "main_board": main_board}
    print(data)
    conn.send(pickle.dumps(data))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(BYTES_TO_RECEIVE))
            players[player_num] = data["player"]

            if players[player_num].is_ready and not players[player_num].in_game and not main_board.game_started:
                players[player_num].in_game = True
                players[player_num].joined_game = True
                main_board.add_player_info(PlayerInfo(name=players[player_num].name, num=player_num, points=0))

            # Process player's answer when submitted
            if players[player_num].answer_chosen and not players[player_num].answer_submitted:
                shape = players[player_num].answer_chosen
                main_board.submit_answer(player=players[player_num], answer=shape)
                players[player_num].answer_submitted = True

            # Send player all related info about answer when the time countdown for a question is up,
            # as determined by the variable 'display_is_answer_correct'
            if players[player_num].display_is_answer_correct:
                players[player_num].reset()
                answer_info = None
                if not players[player_num].got_answer_info:
                    answer_info = main_board.get_answer_info(players[player_num])
                    players[player_num].answer_info = answer_info
                    players[player_num].got_answer_info = True

            reply = {"player": players[player_num], "main_board": main_board}

            # print(f"Received {data}")
            # print(f"Sending {reply}")
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print(type(e))
            print(f"Player {players[player_num]} disconnected")
            main_board.remove_player_info(players[player_num])
            del players[player_num]
            break

def threaded_spammer(conn, settings):
    if settings.is_spammer_enabled:
        print("The network has been infiltrated!!!")

        data = "Empty"
        symbols = "1234567890!@#$%^&*()"
        spammer_number = -1
        spammer_list = []
        conn.send(data.encode())
        try:
            # Create all the spammers
            data = pickle.loads(conn.recv(BYTES_TO_RECEIVE))
            for _ in range(data.times):
                name = data.spam_name + str(random.choice(list(symbols))) + str(random.choice(list(symbols)))
                new_spammer = PlayerInfo(name, spammer_number, 0)
                spammer_list.append(new_spammer)
                main_board.add_player_info(new_spammer)
                spammer_number -= 1
                time.sleep(data.seconds / data.times)

            conn.sendall(pickle.dumps(data))

        except:
            print("Network is back online!")

        while True:
            is_correct_list = [random.randint(0, 1) == 1 for _ in range(len(spammer_list))] # 50% chance the spammer gets the answer correct

            # For each question, stall spammer thread until the answers are displayed
            while not main_board.show_choices_screen:
                pygame.time.delay(100)

            correct_answer = main_board.get_correct_shape()
            incorrect_answers = ["triangle", "diamond", "circle", "square"]
            incorrect_answers.remove(correct_answer)
            for i, is_correct in enumerate(is_correct_list):
                choice = correct_answer

                if not is_correct:
                    choice = random.choice(incorrect_answers)

                if spammer_list[i] in main_board.player_info_list:
                    main_board.submit_answer(spammer_list[i], choice)

            # For each question, stall spammer thread until the answers are displayed
            while not main_board.display_correct_answer:
                pygame.time.delay(100)

            for spammer in spammer_list:
                if spammer in main_board.player_info_list:
                    main_board.get_answer_info(spammer)

            while main_board.show_choices_screen:
                pygame.time.delay(100)

    else:
        data = "Host has disabled spamming!!! Too bad so sad."
        conn.send(data.encode())

def handle_incoming_clients(player, settings):
    while True:
        conn, addr = server.accept()

        # Figure out if the connection is a player or the spammer
        conn.send("Player or spammer?".encode())
        data = conn.recv(BYTES_TO_RECEIVE).decode("utf-8")
        if data == "player":
            players[player] = Player(screen_x=0, screen_y=0, screen_width=CLIENT_WIDTH, screen_height=CLIENT_HEIGHT,
                                     num=player, random_names=random_names)
            _thread.start_new_thread(threaded_player, (conn, player))
            print(f"Player {player} connected to {addr}")
            player += 1
        else:
            _thread.start_new_thread(threaded_spammer, (conn, settings))
            spammer_activated = True

def install_missing_libraries(libraries):
    import importlib
    import subprocess

    for library in libraries:
        try:
            importlib.import_module(library)
        except ImportError:
            subprocess.call(["pip", "install", library])

if __name__ == "__main__":
    install_missing_libraries(libraries=["pygame", "pandas"])

    SERVER = input("Please enter the local IP address of your machine (type ipconfig in command prompt to find it. It's the IP4 address): ")

    # For random name generator if needed
    with open("random_names.txt", "r") as f:
        random_names = f.readlines()
        random_names = [name.strip() for name in random_names]

    # Get all kahoot files from the specific "quizzes" folder
    current_directory = os.getcwd()
    quiz_directory = f"{current_directory}\\Quizzes"
    file_names = [f for f in os.listdir(quiz_directory) if os.path.isfile(os.path.join(quiz_directory, f)) and not f.startswith('~$')]

    print("Kahoot quizzes to choose from:")
    for i, file in enumerate(file_names):
        print(f"{i + 1}. {file.split('.')[0]}")
    print()

    # Ensure host types valid kahoot number corresponding to kahoot quizzes from the "quizzes" folder
    kahoot_quiz_num = input("Please type in the number of the kahoot quiz you want to play: ")
    kahoot_quiz_document = None
    while not kahoot_quiz_document:
        if kahoot_quiz_num.isdigit():
            kahoot_quiz_num = int(kahoot_quiz_num)
            if 1 <= int(kahoot_quiz_num) <= len(file_names):
                kahoot_quiz_document = file_names[int(kahoot_quiz_num) - 1]
            else:
                kahoot_quiz_num = input(f"Number must be between 1 and {len(file_names)} (inclusive): ")
        else:
            kahoot_quiz_num = input(f"Please enter a valid number between 1 and {len(file_names)} (inclusive): ")

    kahoot_quiz = handle_csv_file(f"{quiz_directory}\\{kahoot_quiz_document}")

    main_board = MainBoard(player_info_list=[], x=0, y=0, width=MAIN_BOARD_WIDTH, height=MAIN_BOARD_HEIGHT,
                           kahoot_name=kahoot_quiz["kahoot_name"], questions=kahoot_quiz["question_obj_list"],
                           settings=kahoot_quiz["settings_obj"], random_names=random_names)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((SERVER, PORT))

    except socket.error as e:
        print(e)

    server.listen(2)
    print("Listening for connections")

    player = 0
    spammer_activated = False
    _thread.start_new_thread(handle_incoming_clients, (player, kahoot_quiz["settings_obj"]))

    # Handle server screen and the sound in the main thread
    sound_handler = SoundHandler()
    pygame.init()
    win = pygame.display.set_mode((MAIN_BOARD_WIDTH, MAIN_BOARD_HEIGHT))
    pygame.display.set_caption("Kahoot Board")
    clock = pygame.time.Clock()
    while True:
        # Pygame logic
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        if main_board.handle_menu:
            main_board.handle_menu_screen(win=win, background="purple")

        if main_board.game_started:
            main_board.handle_game(win=win, background="purple")

        if main_board.show_results:
            main_board.handle_results(win=win, background="purple")

        clock.tick(FPS)
        pygame.display.update()

        # Sounds if the settings for the music is "yes"
        if main_board.settings.is_music_enabled:
            if main_board.player_menu_sound:
                sound_handler.play_sound(sound_key="menu", loops=-1)
            if main_board.game_started:
                sound_handler.stop_sound(sound_key="menu")

            if main_board.show_choices_screen and not main_board.display_correct_answer:
                if not sound_handler.get_sound_playing():
                    sound_keys = ["answer_melody1", "answer_melody2", "answer_melody3", "answer_melody4"]
                    random_sound_key = random.choice(sound_keys)
                    sound_handler.play_sound(sound_key=random_sound_key)

            if main_board.display_correct_answer:
                sound_playing = sound_handler.get_sound_playing()
                if sound_playing and sound_playing.sound_key != "is_answer_correct":
                    sound_handler.stop_sound(sound_playing.sound_key)

                if not sound_handler.sounds["is_answer_correct"].is_played:
                    sound_handler.play_sound(sound_key="is_answer_correct")

            if main_board.show_countdown:
                sound_handler.reset_is_played()

            if main_board.show_results:
                sound_handler.play_sound(sound_key="results_music")
