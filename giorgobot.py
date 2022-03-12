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

f = open('emvolioapi.txt', 'r')
emvolioapi = f.read()
f.close()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

skoil = Skoil(client)

#Λίστα μηνυμάτων απόρριψης για την κατηγορία των βιβλιοθηκών
warning1 = "Σσσσσσσσσσσσσσσσσσσσσς! ***ΨΥΘΙΡΣΤΑ*** εδώ είναι βιβλιοθήκη! Δεν κάνει να μιλάμε εδώ..."
warning2 = "Ρε κλόουν. Όχι μηνύματα εδώ. ΜΟΝΟ ΦΩΤΟΓΡΑΦΙΕΣ/ΒΙΝΤΕΟ."
warning3 = "🚓 ΣΥΛΛΑΜΒΑΝΕΣΑΙ, ΒΛΑΚΑΚΟ. ΜΙΛΟΥΣΕΣ ΣΤΗ ΒΙΒΛΙΟΘΗΚΗ. 10 μέρες φυλακή μέχρι να μάθεις να στέλνεις μόνο φωτογραφίες ή βίντεο."
warning4 = "Εδώ. Φωτογραφίες/Βίντεο. ***__ΜΟΝΟ__***. Εχμ, ωραία :)"

warning_messages = [warning1, warning2, warning3, warning4]

#Παράπονα του μποτ, όταν το κάνουν μένσιον
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


def remove_greek_uppercase_accent(x):
    x = x.replace("Ά", "Α")
    x = x.replace("Έ", "Ε")
    x = x.replace("Ή", "Η")
    x = x.replace("Ί", "Ι")
    x = x.replace("Ό", "Ο")
    x = x.replace("Ύ", "Υ")
    x = x.replace("Ώ", "Ω")
    x = x.replace("΅Ι", "Ϊ")
    x = x.replace("Ϊ́", "Ϊ")
    x = x.replace("΅Υ", "Ϋ")
    x = x.replace("Ϋ́", "Ϋ")
    return x

#συναρτήσεις που ευθύνονται για τους ρόλους
async def give_role(member, role):
    if member is not None and role is not None:
        await member.add_roles(role)
        channel_log("Successfully gave role " + role.name + " to member " + member.name)

async def remove_role(member, role):
    if member is not None and role is not None:
        await member.remove_roles(role)
        channel_log("Successfully removed role " + role.name + " from member " + member.name)

async def private_msg(message, sender):
    if '{' in message and message[-1] == '}' and '"target"' in message and '"message"' in message:
        payload = 0
        try:
            payload  = json.loads(message.split("!send ")[1])
        except:
            await sender.send("Είσαι πολύ ηλίθιος, αν δεν ξέρεις ούτε σωστή **JSON** να γράφεις. 😣")
            return

        targetID = False

        server   = client.get_guild(322050982747963392)
        users    = await server.fetch_members().flatten()

        try:
            targetID = [i.id for i in users if str(i) == payload["target"]].pop()
            await sender.send("Αμέσως! Στέλνω μήνυμα προς **" + payload["target"] + "**.")
        except Exception as e:
            print("Unable to decode dictionary.", e.args)
            await sender.send('**ΚΑΤΙ ΠΑΕΙ ΛΑΘΟΣ.**\n\n Σωστός χειρισμός εντολής:\n```json\n{"message":"<μήνυμα>", "target":"<Χρήστης#1234>"}```')
        
        if targetID:
            user_to_send = client.get_user(targetID)
            await user_to_send.send(payload["message"])
            await sender.send("Έφτασε το μήνυμα!")

async def announce(message, sender):
    if '{' in message and message[-1] == '}' and '"channel"' in message and '"message"' in message:
        payload = 0
        try:
            payload  = json.loads(message.split("!send ")[1])
        except:
            await sender.send("Είσαι πολύ ηλίθιος, αν δεν ξέρεις ούτε σωστή **JSON** να γράφεις 🙄")
            return
        targetID = False

        server   = client.get_guild(322050982747963392)
        channels = await server.fetch_channels()

        try:
            targetID = [i.id for i in channels if i.name == payload["channel"]].pop()
            await sender.send("Εννοείται πως θα το ανακοινώσω στο <#" + str(targetID) + ">")
        except Exception as e:
            print("Unable to decode dictionary.", e.args)
            await sender.send("Δεν το βρήκα αυτό ρε φίλε :(")
        
        if targetID:
            channel = client.get_channel(targetID)
            await channel.send(payload["message"])
            await sender.send('**ΝΑΙ, ΑΛΛΑ ΟΧΙ.**\n\n Σωστός χειρισμός εντολής:\n```json\n{"message":"<μήνυμα>", "channel":"akrives-onoma-kanaliou"}```')


@client.event
async def on_ready():
    await skoil.initiate()
    print('Bot online.')

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
        if ctx.channel != skoil.bot_requests:
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

    
possible_command_symbols = ['!', '/', 'pm!', 'skoil ']

@client.event
async def on_message(message):

    #message log.
    channel_log(str(message.author) + " in " + str(message.channel) + " says: " + message.content)

    #never respond to the bot itself.
    if message.author == client.user:
        return

    #execute possible commands.
    await parse_command(message.content, message)

    
        
#Το μέρος, όπου οι χρήστες παίρνουν ρόλο βάσει των reactions τους.
@client.event
async def on_raw_reaction_add(payload):
    #αν δεν αντιστοιχεί το μήνυμα του reaction στο συγκεκριμένο reaction Που θέλουμε, τότε δεν μας ενδιαφέρει καθολου
    if payload.message_id != 761204434670714912:
        return

    #αποθηκεύουμε σε μεταβλητή τον σέρβερ μας
    server  = client.get_guild(payload.guild_id)   
    reactor = payload.member 

    #και μετά ελέγχουμε κάθε πιθανό σενάριο
    if payload.emoji.name == "rainbow_six_siege":
        role = server.get_role(760755925535031357)
    
    elif payload.emoji.name == "rocket_league":
        role = server.get_role(760839558655901767)

    elif payload.emoji.name == "minecraft":
        role = server.get_role(761471771450015755)
    
    elif payload.emoji.name == "forza_horizon4":
        role = server.get_role(761471931631009792)

    elif payload.emoji.name == "gtaV":
        role = server.get_role(813411557341921341)

    elif payload.emoji.name == "among_us":
        role = server.get_role(761472151152230411)
    
    elif payload.emoji.name == "league_of_legends":
        role = server.get_role(761472271239217183)

    elif payload.emoji.name == "euro_truck_sim2":
        role = server.get_role(761472440395497493)

    elif payload.emoji.name == "wow":
        role = server.get_role(770018540618907669)

    elif payload.emoji.name == "sea_of_thieves":
        role = server.get_role(778608259925803009)

    elif payload.emoji.name == "phasmophobia":
        role = server.get_role(780112959811616788)

    elif payload.emoji.name == "pubeg":
        role = server.get_role(813411722903552062)
    
    elif payload.emoji.name == "politics":
        role = server.get_role(819861063213645854)

    elif payload.emoji.name == "valorant":
        role = server.get_role(834504650509254749)

    #ύστερα, δίνουμε τον ρόλο σε αυτόν που έκανε το react με την φτιαχτή συνάρτησή μας
    await give_role(reactor, role)

@client.event
async def on_raw_reaction_remove(payload):
    #αν δεν αντιστοιχεί το μήνυμα του reaction στο συγκεκριμένο reaction Που θέλουμε, τότε δεν μας ενδιαφέρει καθολου
    if payload.message_id != 761204434670714912:
        return

    #αποθηκεύουμε σε μεταβλητή τον σέρβερ μας
    server  = client.get_guild(payload.guild_id)

    #είναι διαφορετικός ο τρόπος, σε σχέση με πάνω, που παίρνουμε τον reactor.   
    reactor = await server.fetch_member(payload.user_id)

    #και μετά ελέγχουμε κάθε πιθανό σενάριο
    if payload.emoji.name == "rainbow_six_siege":
        role = server.get_role(760755925535031357)
    
    elif payload.emoji.name == "rocket_league":
        role = server.get_role(760839558655901767)

    elif payload.emoji.name == "minecraft":
        role = server.get_role(761471771450015755)
    
    elif payload.emoji.name == "forza_horizon4":
        role = server.get_role(761471931631009792)
    
    elif payload.emoji.name == "gtaV":
        role = server.get_role(813411557341921341)

    elif payload.emoji.name == "among_us":
        role = server.get_role(761472151152230411)
    
    elif payload.emoji.name == "league_of_legends":
        role = server.get_role(761472271239217183)

    elif payload.emoji.name == "euro_truck_sim2":
        role = server.get_role(761472440395497493)

    elif payload.emoji.name == "wow":
        role = server.get_role(770018540618907669)

    elif payload.emoji.name == "sea_of_thieves":
        role = server.get_role(778608259925803009)

    elif payload.emoji.name == "phasmophobia":
        role = server.get_role(780112959811616788)

    elif payload.emoji.name == "pubeg":
        role = server.get_role(813411722903552062)
    
    elif payload.emoji.name == "politics":
        role = server.get_role(819861063213645854)

    elif payload.emoji.name == "valorant":
        role = server.get_role(834504650509254749)

    #ύστερα, βγάζουμε τον ρόλο σε αυτόν που έκανε το react με την φτιαχτή συνάρτησή μας
    await remove_role(reactor, role)

client.run(token)