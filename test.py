from datetime import date


command = "giorg corona gr"

def parser(command : str):

    command_symbol = "giorg "

    if not command.startswith(command_symbol):
        return

    command = command[len(command_symbol):]

    command_dict = {
        'display_members' : None,
        'secret_santa'    : None,
        'ping'            : None,
        'help'            : None,
        'announce_bot'    : None,
        'announce_geniki' : None,
        'announce'        : [str],
        'prune'           : [int],
        'corona'          : [str, date],
        'emvolio'         : [str, date]
    }
    
    #check if command exists.
    command_call = [i for i in command_dict if command.startswith(i)]
    if len(command_call) == 0:
        print("Command doesn't exist.")
        return
    
    #if it exists take it.
    command_call = command_call.pop()
    
    #see if it has arguments
    if command_dict[command_call] is None:
        print("Command has no arguments. Calling command...")
        return

    #and if it does have arguments, see if it is the right length 
    parameters = command.split(" ")[1:]
    if len(parameters) < 1:
        print("wrong arguements.")

    print(parameters)


    
parser(command)