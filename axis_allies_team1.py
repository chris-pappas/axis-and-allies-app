import copy
import json
import random

def is_cracked(path_to_check):
    '''
    Returns True if "cracked", False if "not_cracked"
    '''
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    cracked_value = data['security']

    if cracked_value == "cracked":
        return True
    return False


def encrypt_future_messages(path_to_check, current_turn):
    '''
    Changes the cracked value of your json file to not_cracked.
    Also updates current turn's message_security value to not_cracked.
    '''
    # json file update
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    data['security'] = "not_cracked"
    
    json_output = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    save_json_file(path_to_check, json_output)

    current_turn['message_security'] = "not_cracked"


def crack_past_messages(path_to_check):
    '''
    Opens up json changing all message security entries to cracked
    '''
    
    #json file update
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    data['security'] = "cracked"
    #print type(data[1])
    for turn in data['turns']:
        turn['message_security'] = "cracked"

    json_output = json.dumps(data,  sort_keys=True, indent=4, separators=(',', ': '))
    save_json_file(path_to_check, json_output)


def successful_crack_attempt(numerator, denominator):
    '''
    Use randint to see if crack attempt is successful.

    Your chances are something like 4/48 (numerator/denominator).
    If the randint is less than or equal to the numerator, success.
    For example, if you have a 4/48 chance, if the randint created
    with range 1-48 is 1,2,3,or 4, it's successful.
    '''

    crack_roll = random.randint(1, denominator)
    if crack_roll <= numerator:
        print("Cracking enemy code encryption...")
        return True
    print("Unable to crack enemy code.")
    return False


def read_stored_messages(path_to_check):
    '''
    Reads all messages from JSON file
    '''

    # json file update
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    for turn in data['turns']:
        print('\n')
        print(turn['turn'])
        if turn['message_security'] == 'cracked':
            for message in turn['messages']:
                print(' -- {}'.format(message))
        
    
def save_json_file(path_to_save, json_data):
    '''
    Takes a path and JSON data and write it to the path
    '''
    
    with open(path_to_save, 'w') as save_file:
        save_file.write(json_data)


def print_menu_banner(turn, country, team):
    
    print '''

=====================================
Welcome to the %s Comm Link.
You are currently on turn: %s - %s

Commands
m - Send a message.
read - Read enemy communications.
crack - Try to crack your opponents' encryption (once per turn).
encrypt - Pay IPCs to re-encrypt messages from this turn on (until cracked again).
end turn - Ends your turn (saving your messages to the log).
close program - closes the program
=====================================
''' % (team, turn, country)

 
def main():

    team_pick = False
    while not team_pick:
        command = raw_input("Welcome to the game!!! Which team are you? Answer 'Axis' or 'Allies': ").lower()
        if command == "axis":
            your_team = command
            team_pick = True
        elif command == "allies":
            your_team = command
            team_pick =  True
        else:
            print("Please type 'axis' or 'allies'")

    if your_team == "axis":
        basic_crack_chance_num = 4
        basic_crack_chance_den = 48
    elif your_team == "allies":
        basic_crack_chance_num = 3
        basic_crack_chance_den = 48
        
    # set paths to json files
    ## path to team 1
    your_team_path = "c:/Python27/axis_and_allies.json"
        
    ## path to team 2
    opponent_team_path = "c:/Python27/axis_stuff.json"

    # list of countries
    round_list = [
        "Germany",
        "Soviet Union",
        "Japan",
        "United States",
        "China",
        "United Kingdom",
        "Italy",
        "Anzac"
    ]
    round_index = 0

    # initialize turn counter
    turn = 1
    teamname = "default_teamname"

    # initialize datatype to organize important game info
    turn_string = "turn%s-%s" % (str(turn), round_list[round_index])
    turn_template = {
        'teamname': teamname,
        'message_security': "not_cracked",
        'messages': [],
        'turn': turn_string.replace(' ', '_'),
        'crack_attempt': False,
    }
 
    # at the beginning of each game, initialize the game file
    game_info = {
        'security': "not_cracked",
        'turns': [],
    }
    json_output = json.dumps(
        game_info,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )
    save_json_file(your_team_path, json_output)
 
    current_turn = copy.deepcopy(turn_template)
    
    # main game menu
    while True:

        print_menu_banner(turn, round_list[round_index], your_team)
        
        command = raw_input("Please enter a command: ").strip()
        if command == "m":
            message = raw_input("Begin typing message text: ")
            current_turn['messages'].append(message)
        
        elif command == "encrypt":
            confirmation =  raw_input("Are you sure you want to spend IPCs to apply new message encryption? (y/n): ")

            if confirmation == "y":
                encrypt_future_messages(your_team_path, current_turn)
                print("\nMessage encryption updated!")
            elif confirmation == "n":
                print("\nMessage encryption not updated.")
            else:
                print("\nPlease answer with 'y' for yes or 'n' for no.")

        elif command == "end turn":
            print("\nYou have ended your turn.")
            
            game_info['turns'].append(current_turn)

            if is_cracked(your_team_path):
                for entry in game_info['turns']:
                    entry['message_security'] = "cracked"

            json_output = json.dumps(
                game_info,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
    
            save_json_file(your_team_path, json_output)
                           
            # End of turn incrementing etc
            turn += 1
            round_index += 1
            if round_index > 7:
                round_index = 0
            turn_string = "turn%s-%s" % (str(turn), round_list[round_index])

            current_turn = copy.deepcopy(turn_template)
            current_turn['turn'] = turn_string.replace(' ', '_')

        elif command == "crack":
            #get one crack attempt per turn
            if not current_turn['crack_attempt']:
                
                confirmation =  raw_input("Would you like to spend IPCs to increase your odds of cracking\nthe enemy's code? (y/n): ")

                if confirmation == "y":
                    ipc_spend_menu = True
                    while ipc_spend_menu:
                        ipc_to_numerator_map = {
                            '5': 8,
                            '10': 16,
                            '15': 23,
                            '20': 31,
                            '25': 39,
                            '30': 46,
                        }
                        ipcs_value = raw_input("How many IPCs would you like to spend? 5/10/15/20/25/30 for 16%/32%/48%/64%/80%/96% increase?")
                        if ipcs_value in ['5', '10', '15', '20', '25', '30',]:
                            print("\nAttempting to crack code with increased odds...")
                            
                            new_crack_chance_num = basic_crack_chance_num + ipc_to_numerator_map[ipcs_value]
                            if successful_crack_attempt(new_crack_chance_num, basic_crack_chance_den):
                                crack_past_messages(opponent_team_path)
                            current_turn['crack_attempt'] = True
                            ipc_spend_menu = False
                            
                        else:
                            print("\nPlease enter any of the following values: 5,10,15,20,25,30")

                elif confirmation == "n":
                    print("\nAttempting to crack their code without increased odds...")
                    # run regular chances here
                    crack_roll = random.randint(1, basic_crack_chance_den)
                    if crack_roll <= basic_crack_chance_num:
                        print("\nCracking enemy come encryption...")
                        crack_past_messages(opponent_team_path)
                    else:
                        print("\nUnable to crack enemy code.")

                    current_turn['crack_attempt'] = True
                    
                else:
                    print("\nPlease answer with 'y' for yes or 'n' for no.")
                
            else:
                print("\nYou can only try to crack the enemy's code once per turn.")

        elif command == "read":
            print("\nReading enemy communications...")

            if is_cracked(opponent_team_path):
                read_stored_messages(opponent_team_path)
            else:
                print("\nYour enemy's communication channels are encrypted.")
    
        elif command == "close program":
            return False
        else:
            print("\nDid not recognize command.")
            
main()
