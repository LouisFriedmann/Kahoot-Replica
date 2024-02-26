import pandas as pd
from main_board import Question, Settings

# handle_csv.py handles all information about the kahoot to play
def handle_csv_file(kahoot_file):
    kahoot_document = kahoot_file.split("\\")[-1]

    kahoot_name = kahoot_document.split(".")[0]

    csv_handled = False
    question_obj_list = []
    settings_obj = None
    while not csv_handled:
        try:
            df = pd.read_csv(kahoot_file, dtype=str)

            # Make a list of Question objects, each object containing the question, the choices, correct choice, and point value
            number_of_questions = len(df["Question"].dropna().to_list())
            question_list = df["Question"].dropna().tolist()
            triangle_list = df["Triangle"].dropna().tolist()
            diamond_list = df["Diamond"].dropna().tolist()
            circle_list = df["Circle"].dropna().tolist()
            square_list = df["Square"].dropna().tolist()
            correct_shape_list = df["Correct Shape"].dropna().tolist()

            points_list = df["Points For Question"].dropna().tolist()
            seconds_list = df["Seconds For Question"].dropna().tolist()

            # Store all kahoot settings in settings object
            settings = df["Kahoot Settings"].dropna().tolist()
            answers = df["Yes or No"].dropna().tolist()
            answers = [answer.lower() for answer in answers]
            settings_answers = dict()

            # After checking for exceptions, ensure that there is valid information in each column
            is_valid_kahoot_name = len(kahoot_name) <= 25
            are_questions_valid = len([question for question in question_list if len(question) > 100]) == 0 and len([question for question in question_list if any(len(word) > 25 for word in question.split())]) == 0
            are_answers_valid = all(len(str(word)) <= 25 for word in triangle_list) and all(len(str(word)) <= 25 for word in diamond_list) and all(len(str(word)) <= 25 for word in circle_list) and all(len(str(word)) <= 25 for word in square_list)
            are_correct_shapes_valid = correct_shape_list.count("Triangle") + correct_shape_list.count("Diamond") + correct_shape_list.count("Circle") + correct_shape_list.count("Square") == len(correct_shape_list)
            is_yes_or_no_valid = answers.count("yes") + answers.count("no") == len(settings) and answers.count("yes") + answers.count("no") == len(answers)
            are_points_valid = not False in [str(point_value).isdigit() for point_value in points_list] and len([point_value for point_value in points_list if int(point_value) < 0 or int(point_value) > 10000]) == 0
            are_seconds_valid = not False in [str(seconds).isdigit() for seconds in seconds_list] and len([seconds for seconds in seconds_list if int(seconds) < 0 or int(seconds) > 60]) == 0
            if not is_valid_kahoot_name:
                input("Kahoot name must be less than or equal to 25 characters. Please rename the excel document, save, come back, and press enter:")

            elif not are_questions_valid:
                input("Each question must be less than or equal to 100 characters and each word must be less than or equal to 25 characters. Please fix this, save, come back, and press enter:")

            elif not are_answers_valid:
                input("Each answer must be less than or equal to 25 characters. Please fix this, save, come back, and press enter:")

            elif not are_correct_shapes_valid:
                input("Correct shape column can only contain these values: \"Triangle\", \"Diamond\", \"Circle\", and \"Square\". Please fix this, save, come back, and press enter:")

            elif not are_points_valid:
                input("Point values must contain all positive integers less than or equal to 10,000. Please fix this, save, come back, and press enter:")

            elif not is_yes_or_no_valid:
                input("Yes or No column should only contain the answers: \"yes\" or \"no\". Please fix this, save, come back, and press enter:")

            elif not are_seconds_valid:
                input("Seconds column must contain all positive integers less than or equal to 60. Please fix this, save, come back, and press enter:")
            else:
                for i in range(len(settings)):
                    if answers[i] == "yes":
                        settings_answers[settings[i]] = True
                    else:
                        settings_answers[settings[i]] = False

                settings_obj = Settings(is_random=settings_answers["Random name generator?"], is_spammer_enabled=settings_answers["Enable spammer?"],
                                        is_music_enabled=settings_answers["Music?"])

                points_list = [int(point_value) for point_value in points_list]
                seconds_list = [int(second_value) for second_value in seconds_list]
                for i in range(number_of_questions):
                    question_obj_list.append(Question(question_list[i], triangle_list[i], diamond_list[i],
                                                      circle_list[i], square_list[i], correct_shape_list[i],
                                                      points_list[i], seconds_list[i]))

                csv_handled = True
        except ValueError:
            input("Some issue that cannot be found is in the document. Please fix it, save, come back, and press enter:")

    return {"kahoot_name": kahoot_name, "question_obj_list": question_obj_list, "settings_obj": settings_obj}

