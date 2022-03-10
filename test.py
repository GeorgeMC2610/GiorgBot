from datetime import date
from commands.admin import Admin
from commands.common import Common
from skoil.skoil import Skoil


command = "giorg ping"

def parser(command : str, caller):

    #in order to call the command, it must have the correct symbol.
    command_symbol = "giorg "
    if not command.startswith(command_symbol):
        return

    command = command[len(command_symbol):]

    #commands for common use
    common_dict = {
        'ping'            : None,
        'help'            : None,
        'corona'          : [str, date],
        'emvolio'         : [str, date]
    }

    #commands for admins only
    admin_dict = {
        'announce_bot'    : None,
        'announce_geniki' : None,
        'announce'        : [str],
        'prune'           : [int],
        'display_members' : None,
        'secret_santa'    : None,
    }
    
    #check if command exists.
    common_command_call = [i for i in common_dict if command.startswith(i)]
    admin_command_call = [i for i in admin_dict if command.startswith(i)]

    #if the command is common use
    if len(common_command_call) != 0:
        
        #take the command
        common_command_call = common_command_call.pop()

        #take the command and examine any possible parameters. If there aren't any, then call the command.
        if common_dict[common_command_call] is None:
            getattr(Common, common_command_call)()

        #if there are parameters, make sure they're right
        else:
            parameters = command.split(" ")[1:]
            if len(parameters) < 1:
                print("wrong arguements.")
                return

            getattr(Common, common_command_call)(parameters)
    else:

        #again, take the command
        admin_command_call = admin_command_call.pop()

        #take the command and examine any possible parameters. If there aren't any, call the command.
        if admin_dict[admin_command_call] is None:
            getattr(Admin, admin_command_call)()

        #if there are parameters, make sure they're right
        else:
            parameters = command.split(" ")[1:]
            if len(parameters) < 1:
                print("wrong arguements.")
                return
            
            getattr(Admin, admin_command_call)(parameters)

parser(command, "foo")