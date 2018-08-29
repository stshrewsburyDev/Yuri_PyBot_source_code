"""
Utils For Yuri PyBot
Made By Steven Shrewsbury (AKA: stshrewsburyDev)
"""

import re, random, json

def reverse(text):
    reversed = ""
    for x in range((len(text)-1), -1, -1):
        reversed += list(text)[x]
    return reversed

def analyse(text):
    analyse_results = {}
    words = text.split()
    number_count = 0
    lowercase = 0
    uppercase = 0
    space_count = 0
    for character in text:
        number_check = re.match("[0-9]", character)
        uppercase_check = re.match("[A-Z]", character)
        lowercase_check = re.match("[a-z]", character)
        if number_check is not None:
            number_count += 1
        if uppercase_check is not None:
            uppercase += 1
        if lowercase_check is not None:
            lowercase += 1

    analyse_results["length"] = str(len(text)) + " Characters"
    analyse_results["numbers"] = str(number_count) + " Characters"
    analyse_results["uppercase"] = str(uppercase) + " Characters"
    analyse_results["lowercase"] = str(lowercase) + " Characters"
    analyse_results["words"] = str(len(words))

    return analyse_results

def checkbin(number):
    if number is None:
        return False
    dashes = 0
    for character in str(number):
        if character == "-":
            dashes += 1
    if dashes >= 2:
        return False
    num_list = list(number)
    if num_list[0] == "-":
        bin_num = number.split("-")
    else:
        bin_num = ["", str(number)]
    for num in str(bin_num[1]):
        if num != "1" and num != "0":
            return False
            break
        else:
            pass
    return True

def num2binconv(number):
    if number >= 0:
        binary_number = bin(number)[2:]
    else:
        binary_number = "-" + str(bin(number)[3:])

    return binary_number

def bin2numconv(number):
    number = int(number)
    if number == 0:
        denary_number = "0"
    elif number >= 1:
        denary_number = str(int(str(number), 2))
    elif number <= -1:
        denary_number = str(int(str(number), 2))

    return denary_number

def rps_get_emoji(rps):
    if rps.lower() == "rock":
        return ":fist:"

    elif rps.lower() == "paper":
        return ":raised_hand:"

    elif rps.lower() == "scissors":
        return ":scissors:"

def fruit_machine_results_maker(possible_outcomes):
    outcome = {}

    outcome_line_1 = [random.choice(possible_outcomes),
                      random.choice(possible_outcomes),
                      random.choice(possible_outcomes)
                      ]
    outcome_line_2 = [random.choice(possible_outcomes),
                      random.choice(possible_outcomes),
                      random.choice(possible_outcomes)
                      ]
    outcome_line_3 = [random.choice(possible_outcomes),
                      random.choice(possible_outcomes),
                      random.choice(possible_outcomes)
                      ]

    outcome["middle_line"] = outcome_line_2

    outcome_text = ":black_circle: " + outcome_line_1[0] + outcome_line_1[1] + outcome_line_1[2] + ":black_circle: \n:arrow_right: " + outcome_line_2[0] + outcome_line_2[1] + outcome_line_2[2] + ":arrow_left: \n:black_circle: " + outcome_line_3[0] + outcome_line_3[1] + outcome_line_3[2] + ":black_circle:"

    outcome["text"] = outcome_text

    return outcome

def re_draw_horse_race(horse_1, horse_2, horse_3, horse_4):
    race = ""

    race += ":one: - "
    for x in range(0, horse_1):
        race += ":black_circle:"
    race += ":horse_racing:"
    for x in range(horse_1, 10):
        race += ":black_circle:"
    race += ":triangular_flag_on_post: \n"

    race += ":two: - "
    for x in range(0, horse_2):
        race += ":black_circle:"
    race += ":horse_racing:"
    for x in range(horse_2, 10):
        race += ":black_circle:"
    race += ":triangular_flag_on_post: \n"

    race += ":three: - "
    for x in range(0, horse_3):
        race += ":black_circle:"
    race += ":horse_racing:"
    for x in range(horse_3, 10):
        race += ":black_circle:"
    race += ":triangular_flag_on_post: \n"

    race += ":four: - "
    for x in range(0, horse_4):
        race += ":black_circle:"
    race += ":horse_racing:"
    for x in range(horse_4, 10):
        race += ":black_circle:"
    race += ":triangular_flag_on_post: \nPlease Wait..."

    return race
