import discord
import random
import datetime
from discord.flags import Intents
import requests
import json
import locale
import flag
from dateutil.parser import parse
from commands.admin import Admin
from commands.common import Common
from skoil.skoil import Skoil

#Εφ' όσον το repository θέλουμε να 'ναι public, πρέπει να αποθηκεύσουμε το token σε ένα ξεχωριστό αρχείο, το οποίο δεν θα συμπεριληφθεί στο repository.
f = open('token.txt', 'r')
token = f.read()
f.close()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

skoil = Skoil(client)

#library complaints
warning1 = "Σσσσσσσσσσσσσσσσσσσσσς! ***ΨΥΘΙΡΣΤΑ*** εδώ είναι βιβλιοθήκη! Δεν κάνει να μιλάμε εδώ..."
warning2 = "Ρε κλόουν. Όχι μηνύματα εδώ. ΜΟΝΟ ΦΩΤΟΓΡΑΦΙΕΣ/ΒΙΝΤΕΟ."
warning3 = "🚓 ΣΥΛΛΑΜΒΑΝΕΣΑΙ, ΒΛΑΚΑΚΟ. ΜΙΛΟΥΣΕΣ ΣΤΗ ΒΙΒΛΙΟΘΗΚΗ. 10 μέρες φυλακή μέχρι να μάθεις να στέλνεις μόνο φωτογραφίες ή βίντεο."
warning4 = "Εδώ. Φωτογραφίες/Βίντεο. ***__ΜΟΝΟ__***. Εχμ, ωραία :)"

warning_messages = [warning1, warning2, warning3, warning4]

#complaints for mentions
plaint1 = "Τιιιιι;"
plaint2 = "ΤΙ ΘΕΕΕΕΣ;"
plaint3 = "Τι έκανα πάλι;"
plaint4 = "ΣΚΑΣΕΕΕΕΕ."
plaint5 = "Άλλη μία φορά να το πεις αυτό και θα σε διώξω."
plaint6 = "Όχι."
plaint7 = "Πω, ρε μαλάκα αλήθεια σκάσε..."

complaints = [plaint1, plaint2, plaint3, plaint4, plaint5, plaint6, plaint7]


def channel_log(message):
    f = open('log.txt', 'a', encoding='utf-8')
    f.write("[" + str(datetime.datetime.now())[:19] + "]: " + message + "\n")
    print("[" + str(datetime.datetime.now())[:19] + "]: " + message)
    f.close()


@client.event
async def on_ready():
    await skoil.initiate()
    print('Bot online.')


@client.event
async def on_message(message):

    #message log.
    channel_log(str(message.author) + " in " + str(message.channel) + " says: " + message.content)

    #never respond to the bot itself.
    if message.author == client.user:
        return
    
    #log the message for pm's
    if message.channel.type == discord.ChannelType.private and message.author != skoil.GeorgeMC2610:
        await skoil.GeorgeMC2610.send("📨 **__PM with " + str(message.author) + "__**: " + message.content)

    #remove any messages from unwanted categories
    if message.channel.type != discord.ChannelType.private and message.channel.category_id == 749958245203836939 and not message.attachments:
        random_warning_message = random.choice(warning_messages)
        await message.delete()
        await message.channel.send(random_warning_message, delete_after=8.0)
        return

    #send random complaints if the bot is mentioned
    if message.channel.type != discord.ChannelType.private and client.user.mentioned_in(message):
        await message.channel.send(random.choice(complaints))
        return



    #execute possible commands.
    await parse_command(message.content, message)


async def parse_command(command : str, ctx):

    #in order to call the command, it must have the correct symbol.
    command_symbol = "giorg "
    if not command.startswith(command_symbol):
        return

    command = command[len(command_symbol):]

    #commands for common use
    common_dict = {
        'ping'            : None,
        'help'            : None,
        'corona'          : [str, datetime],
        'emvolio'         : [str, datetime]
    }

    #commands for admins only
    admin_dict = {
        'send'            : [str],
        'announce'        : [str],
        'announce_bot'    : [str],
        'announce_geniki' : [str],
        'prune'           : [int],
        'display_members' : None,
        'secret_santa'    : None,
    }
    
    #check if command exists.
    common_command_call = [i for i in common_dict if command.startswith(i)]
    admin_command_call  = [i for i in admin_dict if command.startswith(i)]

    #if the command is common use
    if len(common_command_call) != 0:       

        #the message has to be inside the bot requests channel. If it's not, delete it.
        if ctx.channel.type != discord.ChannelType.private and ctx.channel != skoil.bot_requests:
            await ctx.delete()
            await ctx.channel.send(random.choice(skoil.denying_messages), delete_after=8.0)
            return

        #take the command
        common_command_call = common_command_call.pop()
        common = Common(ctx, skoil)

        #take the command and examine any possible parameters. If there aren't any, then call the command.
        if common_dict[common_command_call] is None:
            await getattr(common, common_command_call)()
            return

        #if there are parameters, make sure they're right
        else:
            parameters = command[(len(common_command_call) + 1):]
            if len(parameters) < 1:
                await ctx.channel.send("Ξέχασες κάτι, βλαμμένε.")
                return

            await getattr(common, common_command_call)(parameters)
            return
    #if the command is admin only
    elif len(admin_command_call) != 0:

        #in private messages only GeorgeMC2610 and Sotiris168 can execute pm commands.
        if ctx.channel.type == discord.ChannelType.private:
            if not(ctx.author == skoil.GeorgeMC2610 or ctx.author == skoil.Sotiris168):
                await ctx.author.send(random.choice(skoil.pm_denying))
                await skoil.GeorgeMC2610.send("Για δες τι κάνει ο " + ctx.author.name + "... Δεν μ' αρέσουν αυτά.")
                return
        #but admin commands can be executed by mods also. So we need a member position of at least 4.
        elif skoil.identify_member_position(ctx.author) < 4:
            await ctx.channel.send("Καλή προσπάθεια, " + ctx.author.mention + "! Αυτή είναι εντολή διαχειριστή. Θα 'ταν κρίμα να το μάθαιναν οι " + skoil.metzi_tou_neoukti.mention + "...")
            return

        #again, take the command
        admin_command_call = admin_command_call.pop()
        admin = Admin(ctx, skoil)      #the object called here will check to see if the message author has admin previleges.

        #take the command and examine any possible parameters. If there aren't any, call the command.
        if admin_dict[admin_command_call] is None:
            await getattr(admin, admin_command_call)()
            return

        #if there are parameters, make sure they're right
        else:
            parameters = command[(len(admin_command_call) + 1):]
            if len(parameters) < 1:
                await ctx.channel.send("Υποτίθεται ότι είσαι και admin/mod και ξέρεις να χρησιμοποιείς και commands 🤡. (δες `/help` αν είσαι εντελώς άχρηστος)")
                return
            
            await getattr(admin, admin_command_call)(parameters)
            return
    
    await ctx.channel.send("Δεν υπάρχει αυτό που λες, ηλίθιε.")
    

### COROUTINES FOR ROLE ASSIGNMENTS / REMOVALS ###

def get_reaction_role(emoji : str) -> int:

    if emoji == "rainbow_six_siege":
        return 760755925535031357
    
    elif emoji == "rocket_league":
        return 760839558655901767

    elif emoji == "minecraft":
        return 761471771450015755

    elif emoji == "forza_horizon4":
        return 761471931631009792

    elif emoji == "gtaV":
        return 813411557341921341

    elif emoji == "among_us":
        return 761472151152230411
    
    elif emoji == "league_of_legends":
        return 761472271239217183

    elif emoji == "euro_truck_sim2":
        return 761472440395497493

    elif emoji == "wow":
        return 770018540618907669

    elif emoji == "sea_of_thieves":
        return 778608259925803009

    elif emoji == "phasmophobia":
        return 780112959811616788

    elif emoji == "pubeg":
        return 813411722903552062
    
    elif emoji == "politics":
        return 819861063213645854

    elif emoji == "valorant":
        return 834504650509254749

    elif emoji == "payday2":
        return 946869439578669089 

    elif emoji == "ktane":
        return 952360700410490880

@client.event
async def on_raw_reaction_add(payload):

    #this is for assigning roles with corresponding emojis. if the message is not the one we're looking for, pass.
    if payload.message_id != 761204434670714912:
        return

    role = skoil.guild.get_role(get_reaction_role(payload.emoji.name))
    await give_role(payload.member, role)

@client.event
async def on_raw_reaction_remove(payload):
    
    #this is for removing roles with corresponding emojis. if the message is not the one we're looking for, pass.
    if payload.message_id != 761204434670714912:
        return

    #for some reason, the reactor cannot be retrieved as easily as above. we have to use the coroutine function in order to get it.
    reactor = await skoil.guild.fetch_member(payload.user_id)
    role = skoil.guild.get_role(get_reaction_role(payload.emoji.name))

    await remove_role(reactor, role)

#coroutine for giving roles
async def give_role(member, role):
    if member is not None and role is not None:
        await member.add_roles(role)
        channel_log("Successfully gave role " + role.name + " to member " + member.name)

#coroutine for removing roles
async def remove_role(member, role):
    if member is not None and role is not None:
        await member.remove_roles(role)
        channel_log("Successfully removed role " + role.name + " from member " + member.name)

#run the bot
client.run(token)