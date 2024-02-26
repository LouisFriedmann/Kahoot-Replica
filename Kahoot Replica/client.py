# client.py contains all information for a kahoot player
import pygame

from network import Network

# Width and height of client's screen
WIDTH, HEIGHT = 800, 600

SECONDS_PER_QUESTION = 30

FPS = 30
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

    server = input("Please enter the IP4 address of the server you are connecting to: ")
    network = Network(server)
    data = network.get_data()
    # Tell the server this is a player
    data = network.send("player")

    player = data["player"]
    main_board = data["main_board"]

    pygame.init()

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kahoot")

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    i = 0
    while running:
        data = network.send(data)
        player = data["player"]
        main_board = data["main_board"]

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update the player screen based on main_board
        if main_board.show_quiz_name:
            player.display_waiting_to_start_screen = False
            player.display_get_ready_screen = True

        if main_board.show_countdown and main_board.is_quiz_img_done_moving:
            player.display_get_ready_screen = False
            player.answer_info = None # Reset answer info before the countdown
            player.handle_countdown_screen(win=win, background_color="yellow",
                                           countdown_seconds=5)

        if main_board.show_choices_screen and not player.answer_chosen:
            player.display_answer_choices = True

        elif player.answer_chosen:
            player.display_answer_choices = False
            player.display_kahoot_phrase = True

        if main_board.display_correct_answer:
            if player.display_answer_choices:
                player.display_answer_choices = False
            else:
                player.display_kahoot_phrase = False

            player.display_is_answer_correct = True


        # Handle when to display which player screen
        if main_board.game_started and not player.in_game:
            player.handle_locked_screen(win=win, background_color="purple")

        elif not player in main_board.player_info_list and player.joined_game:
            player.in_game = False
            player.is_ready = False
            player.handle_nickname_screen(win=win, pygame_events=events, is_random=False, background_color="purple",
                                          is_kicked=True, random_names=main_board.random_names)

        else:
            if player.display_is_answer_correct:
                if player.answer_info:
                    player.handle_is_answer_correct(win, player.answer_info)

            if player.display_kahoot_phrase:
                player.handle_kahoot_phrase(win=win, phrases=main_board.kahoot_phrases)

            if player.display_answer_choices:
                player.handle_answer_choices(win)

            if player.display_get_ready_screen:
                player.handle_get_ready_screen(win)

            if player.display_waiting_to_start_screen:
                if player in main_board.player_info_list:
                    main_board.player_info_list[main_board.player_info_list.index(player)].kick_me = False
                player.handle_waiting_to_start_screen(win=win, background_color="green")

            if player.display_nickname_screen:
                player.handle_nickname_screen(win=win, pygame_events=events, is_random=main_board.settings.is_random, background_color="purple", is_kicked=False, random_names=main_board.random_names)


        data = {"player": player, "main_board": main_board}

        clock.tick(FPS)

        pygame.display.update()

    pygame.quit()
