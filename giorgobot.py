import discord
import random
import datetime
from dateutil.parser import parse
from commands.admin import Admin
from commands.common import Common
from skoil.skoil import Skoil

#Εφ' όσον το repository θέλουμε να 'ναι public, πρέπει να αποθηκεύσουμε το token σε ένα ξεχωριστό αρχείο, το οποίο δεν θα συμπεριληφθεί στο repository.
f = open('token.txt', 'r')
token = f.read()
f.close()

intents = discord.Intents.all()
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
    await assign_starting_roles()

    print('Bot online.')



@client.event
async def on_message(message):

    #message log.
    channel_log(str(message.author) + " in " + str(message.channel) + " says: " + message.content)

    #never respond to the bot itself.
    if message.author == client.user:
        return
    
    #messages in server
    if message.channel.type != discord.ChannelType.private:

        #delete every message in unwated categories.
        if message.channel.category_id == 749958245203836939 and not message.attachments:
            random_warning_message = random.choice(warning_messages)
            await message.delete()
            await message.channel.send(random_warning_message, delete_after=8.0)
            return  #don't execute possible commands.

        #random meme with backstory.
        elif 'nibbaebi'.casefold() in message.content.casefold():
            await message.author.move_to(None)
            await message.reply("Give this mothafucka a 27 minute ban for being toxic. I'm French. (Κατουράω το Miliobot).", mention_author=True)
            return

        #send a random meme complaint if the bot is mentioned.
        elif client.user.mentioned_in(message):
            await message.reply(random.choice(complaints), mention_author=True)
            return
            
    #private messages
    else:

        #for every message author that is not GeorgeMC2610, send pm to GeorgeMC2610 containing the author's message content.
        if message.author != skoil.GeorgeMC2610:
            await skoil.GeorgeMC2610.send("📨 **__PM with " + str(message.author) + "__**: " + message.content)

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
        'add_library'     : [int],
        'remove_library'  : [int]
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
    
#assign missing roles for when the bot is offline.
async def assign_starting_roles():

    #get the correct message
    acquire_a_role = await skoil.guild.fetch_channel(760736083544637511)
    message = await acquire_a_role.fetch_message(761204434670714912)
    
    #get its reactions
    for reaction in message.reactions:

        #fetch the role that is missing
        role = skoil.guild.get_role(get_reaction_role(reaction.emoji.name))
        print(f"Now seeking for {role.name}.")

        #get all the users that HAVE reacted to this message
        users_reacted = [user async for user in reaction.users()]

        #get all the users that HAVE NOT reacted to this message
        all_users = [user async for user in skoil.guild.fetch_members()]
        users_not_reacted = list(set(all_users) - set(users_reacted))

        #handle roles respectively
        for user in users_reacted:

            try:
                member = await skoil.guild.fetch_member(user.id)
                await give_role(member, role, log=False)
            except Exception as e:
                print(f"Error with member {user} (Possibly not found).", e.args)
        
        for user in users_not_reacted:

            try:
                member = await skoil.guild.fetch_member(user.id)
                await remove_role(member, role, log=False)
            except Exception as e:
                print(f"Error with member {user} (Possibly not found).", e.args)
    
    print("All done! All roles checked.")

    

### COROUTINES FOR ROLE ASSIGNMENTS / REMOVALS ###

def get_reaction_role(emoji : str) -> int:

    roles = {
        "rainbow_six_siege" : 760755925535031357,
        "rocket_league"     : 760839558655901767,
        "minecraft"         : 761471771450015755,
        "forza_horizon4"    : 761471931631009792,
        "gtaV"              : 813411557341921341,
        "among_us"          : 761472151152230411,
        "league_of_legends" : 761472271239217183,
        "euro_truck_sim2"   : 761472440395497493,
        "wow"               : 770018540618907669,
        "sea_of_thieves"    : 778608259925803009,
        "phasmophobia"      : 780112959811616788,
        "pubeg"             : 813411722903552062,
        "politics"          : 819861063213645854,
        "valorant"          : 834504650509254749,
        "payday2"           : 946869439578669089,
        "ktane"             : 952360700410490880,
        "fallguys"          : 993591056711028898
    }

    return roles.get(emoji, None)


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

    #for some unknown reason, the reactor cannot be retrieved as easily as above. we have to use the coroutine function in order to get it.
    reactor = await skoil.guild.fetch_member(payload.user_id)
    role = skoil.guild.get_role(get_reaction_role(payload.emoji.name))

    await remove_role(reactor, role)

#coroutine for giving roles
async def give_role(member, role, log=True):
    if member is not None and role is not None:
        await member.add_roles(role)

        if log:
            channel_log("Successfully gave role " + role.name + " to member " + member.name)

#coroutine for removing roles
async def remove_role(member, role, log=True):
    if member is not None and role is not None:
        await member.remove_roles(role)

        if log:
            channel_log("Successfully removed role " + role.name + " from member " + member.name)

#run the bot
client.run(token)
