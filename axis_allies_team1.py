import string
import sys
import json
import random

### requirements
# 1) interactive window
#
# objective: keep track of all info in a dictionary, or json (probably json)
# keep track of team name, turn #, cracked value, and all text sent

# later, need to be able to take all entries from other teams that have cracked
# value of false, change it to true and print out all their text messages

# when code is reincrypted cracked value for new entries are set to false

# keep information in python data types, and then load to json format before
# writing to file

#list of turns
# germany, soviet union, japan, united states, china, united kingdom, italy,
# anzac
#
#
# Post steve chat to-dos:
# 1)Update rounds 2)get absolute turn number 3)implement cracking features
# a) features to add: i) command to try to crack code (crack attempt - once per turn)
#                   ii) IPC to increase chances of cracking code
# 1) Add country names to turn ids? DONE
# 2) Add ability to crack opponents code DONE
# 3) Add ability to increase your chances of cracking your opponents code
# 4) Add functionality to read all messages that you cracked from opponent DONE

#5 IPCS INCREASES CRACK ODDS BY 16%
#doing X/48 for probs. 4/48 axis and 3/48 allies

def check_if_cracked(path_to_check):
    '''
    Returns True if "cracked", False if "not_cracked"
    '''
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    #print data
    cracked_value = str(data[0])
    #print type(cracked_value)
    #print repr(cracked_value)


    if cracked_value == "cracked":
        #print "it's true"
        return True
    else:
        #print "it's false"
        return False

def encrypt_future_messages(path_to_check,game_info_dict,turn_string):
    '''
    Changes the cracked value of your json file to not_cracked.
    Also updates current turn's message_security value to not_cracked.
    '''
    #json file update
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    data[0] = "not_cracked"

    json_output = json.dumps(data,  sort_keys=True, indent=4, separators=(',', ': '))

    save_json_file(path_to_check, json_output)

    #current turn message_security update
    game_info_dict[turn_string][1] = "not_cracked"
    
def crack_past_messages(path_to_check):
    '''
    Opens up json changing all message security entries to cracked
    '''
    
    #json file update
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    data[0] = "cracked"
    #print type(data[1])
    #for each key in dictionary which hold turn/value pairs
    for key in data[1]:
        #grab the message security value
        #print data[1][key][1]
        data[1][key][1] = str(data[1][key][1])
        data[1][key][1] = "cracked"

    json_output = json.dumps(data,  sort_keys=True, indent=4, separators=(',', ': '))

    save_json_file(path_to_check, json_output)

def attempt_to_crack(numerator, denominator):
    '''
    Use randint to see if crack attempt is successful.

    Your chances are something like 4/48 (numerator/denominator). If the randint is less than or equal to the numerator, success.
    For example, if you have a 4/48 chance, if the randint created with range 1-48 is 1,2,3,or 4, it's successful.
    '''

    crack_roll = random.randint(1,denominator)
    if crack_roll <= numerator:
        print "Cracking enemy come encryption..."
        return True
        
    else:
        print "Unable to crack enemy code."
        return False
        
def read_stored_messages(path_to_check):
    '''
    Reads all messages from JSON file
    '''
    
    #json file update
    with open(path_to_check) as data_file:
        data = json.load(data_file)

    for key in data[1]:
        #print data[1][key][2]
        print key ,
        print " - " ,
        print ', '.join(data[1][key][2])
    
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
    #decide what team you are for probabilities
    while team_pick == False:
        command = raw_input("Welcome to the game!!! Which team are you? Answer 'Axis' or 'Allies': ")
        if command == "Axis":
            your_team = command
            team_pick = True
        elif command == "Allies":
            your_team = command
            team_pick =  True
        else:
            print "Please type 'Axis' or 'Allies'"

    if your_team == "Axis":
        basic_crack_chance_num = 4
        basic_crack_chance_den = 48
    elif your_team == "Allies":
        basic_crack_chance_num = 3
        basic_crack_chance_den = 48


    crack_attempt = 1
        
    # set paths to json files
    ## path to team 1
    your_team_path = "c:/Python27/axis_and_allies.json"
        
    ## path to team 2
    opponent_team_path = "c:/Python27/axis_stuff.json"

    # list of countries
    round_list = ["Germany", "Soviet Union", "Japan", "United States", "China", "United Kingdom", "Italy", "Anzac"]
    round_index = 0


    # initialize turn counter
    turn = 1
    teamname = "default_teamname"
    cracked = "not_cracked"
    message_security = cracked

    
    # initialize datatype to organize important game info
    #
    game_info_dict = {}
    turn_string = "turn%s-%s" % (str(turn), round_list[round_index])
    game_info_dict[turn_string] = [teamname, message_security, ["Beginning of turn."]]

    # at the beginning of each game, intitialize the game file
    json_output = json.dumps([cracked, game_info_dict],  sort_keys=True, indent=4, separators=(',', ': '))
    save_json_file(your_team_path, json_output)
    
    # main game menu
    while True:

        print_menu_banner(turn,round_list[round_index],your_team)

        
        command = raw_input("Please enter a command: ")

        if command == "m":

            message = raw_input("Begin typing message text: ")

            #append to this turn's message log
            game_info_dict[turn_string][2].append(message)
            
        elif command == "encrypt":

            confirmation =  raw_input("Are you sure you want to spend IPCs to apply new message encryption? (y/n):")

            if confirmation == "y":
                encrypt_future_messages(your_team_path, game_info_dict, turn_string)
                print "Message encryption updated!"
                
            elif confirmation == "n":
                print "Message encryption not updated."
            else:
                print "Please answer with 'y' for yes or 'n' for no."
            
        elif command == "end turn":

            print "You have ended your turn."
            #check if they were cracked
            if check_if_cracked(your_team_path) == True:
                #update their cracked and message_security values
                cracked = "cracked"
                message_security = cracked
                for entry in game_info_dict:
                    game_info_dict[entry][1] = message_security
            else:
                cracked = "not_cracked"
                message_security = cracked
                
            json_output = json.dumps([cracked, game_info_dict],  sort_keys=True, indent=4, separators=(',', ': '))

            save_json_file(your_team_path, json_output)
                           
            #increment turn, and make new entry in dictionary
            turn += 1
            round_index += 1
            # reset round counter
            if round_index > 7:
                round_index = 0
            turn_string = "turn%s-%s" % (str(turn), round_list[round_index])
            game_info_dict[turn_string] = [teamname, message_security, ["Beginning of turn."]]

            crack_attempt = 1
            
        elif command == "crack":
            #get one crack attempt per turn
            if crack_attempt == 1:
                
                confirmation =  raw_input("Would you like to spend IPCs to increase your odds of cracking\nthe enemy's code? (y/n):")

                if confirmation == "y":

                    ipc_spend_menu = True
                    while ipc_spend_menu == True:

                        try:
                            how_many_ipcs = input("How many IPCs would you like to spend? 5/10/15/20/25/30 for 16%/32%/48%/64%/80%/96% increase?")

                            #increase numerator by 8
                            if how_many_ipcs == 5:
                                new_crack_chance_num = basic_crack_chance_num + 8
                                print "Attempting to crack code with increased odds..."
                                if attempt_to_crack(new_crack_chance_num, basic_crack_chance_den) == True:
                                    crack_past_messages(opponent_team_path)
                                crack_attempt = 0
                                ipc_spend_menu = False

                            #increase numerator by 16
                            elif how_many_ipcs == 10:
                                new_crack_chance_num = basic_crack_chance_num + 16
                                print "Attempting to crack code with increased odds..."
                                if attempt_to_crack(new_crack_chance_num, basic_crack_chance_den) == True:
                                    crack_past_messages(opponent_team_path)
                                crack_attempt = 0
                                ipc_spend_menu = False

                            #increase numerator by 23
                            elif how_many_ipcs == 15:
                                new_crack_chance_num = basic_crack_chance_num + 23
                                print "Attempting to crack code with increased odds..."
                                crack_roll = random.randint(1,new_crack_chance_num)
                                if attempt_to_crack(new_crack_chance_num, basic_crack_chance_den) == True:
                                    crack_past_messages(opponent_team_path)
                                crack_attempt = 0
                                ipc_spend_menu = False

                            #increase numerator by 31
                            elif how_many_ipcs == 20:
                                new_crack_chance_num = basic_crack_chance_num + 31
                                print "Attempting to crack code with increased odds..."
                                if attempt_to_crack(new_crack_chance_num, basic_crack_chance_den) == True:
                                    crack_past_messages(opponent_team_path)
                                crack_attempt = 0
                                ipc_spend_menu = False

                            #increase numerator by 39
                            elif how_many_ipcs == 25:
                                new_crack_chance_num = basic_crack_chance_num + 39
                                print "Attempting to crack code with increased odds..."
                                if attempt_to_crack(new_crack_chance_num, basic_crack_chance_den) == True:
                                    crack_past_messages(opponent_team_path)
                                crack_attempt = 0
                                ipc_spend_menu = False

                            #increase numerator by 46
                            #always 100% chance in this case no matter what the team
                            elif how_many_ipcs == 30:
                                new_crack_chance_num = basic_crack_chance_num + 46
                                print "Attempting to crack code with increased odds..."
                                if attempt_to_crack(new_crack_chance_num, basic_crack_chance_den) == True:
                                    crack_past_messages(opponent_team_path)
                                crack_attempt = 0
                                ipc_spend_menu = False
                            
                        except:
                            print "Please enter any of the following values: 5,10,15,20,25,30"

                elif confirmation == "n":
                    print "Attemping to crack their code without increased odds..."
                    #run regular chances here
                    crack_roll = random.randint(1,basic_crack_chance_den)
                    if crack_roll <= basic_crack_chance_num:
                        print "Cracking enemy come encryption..."
                        crack_past_messages(opponent_team_path)
                        
                    else:
                        print "Unable to crack enemy code."

                    crack_attempt = 0
                    
                else:
                    print "Please answer with 'y' for yes or 'n' for no."
                
            else:
                print "You can only try to crack the enemy's code once per turn."

        elif command == "read":
            print "Reading enemy communications..."

            if check_if_cracked(opponent_team_path) == True:
                read_stored_messages(opponent_team_path)
            else:
                print "Your enemy's communication channels are encrypted."
                
        elif command == "close program":
            return False

        #elif command == "p":
        #    print game_info_dict[turn_string][2]
           
        
        else:
            print "Did not recognize command."
            
            
main()
