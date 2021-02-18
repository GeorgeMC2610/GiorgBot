import discord
import random
import datetime
from discord.ext import commands, tasks

#Εφ' όσον το repository θέλουμε να 'ναι public, πρέπει να αποθηκεύσουμε το token σε ένα ξεχωριστό αρχείο, το οποίο δεν θα συμπεριληφθεί στο repository.
f = open('token.txt', 'r')
token = f.read()
f.close()

client = discord.Client()

async def give_role(member, role):
    if member is not None and role is not None:
        await member.add_roles(role)
        print("[" + str(datetime.datetime.now()) + "]: Successfully gave role", role.name, "to member", member.name)

async def remove_role(member, role):
    if member is not None and role is not None:
        await member.remove_roles(role)
        print("[" + str(datetime.datetime.now()) + "]: Successfully removed role", role.name, "to member", member.name)
            

#Το μέρος, όπου οι χρήστες παίρνουν ρόλο βάσει των reactions τους.
@client.event
async def on_raw_reaction_add(payload):
    #αν δεν αντιστοιχεί το μήνυμα του reaction στο συγκεκριμένο reaction Που θέλουμε, τότε δεν μας ενδιαφέρει καθολου
    if payload.message_id != 761204434670714912:
        return

    #αλλιώς ξέρουμε σε κάθε περίπτωση ότι είναι ακριβώς το μήνυμα που θέλουμε
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

    #ύστερα, δίνουμε τον ρόλο σε αυτόν που έκανε το react με την φτιαχτή συνάρτησή μας
    await give_role(reactor, role)


@client.event
async def on_raw_reaction_remove(payload):
    #αν δεν αντιστοιχεί το μήνυμα του reaction στο συγκεκριμένο reaction Που θέλουμε, τότε δεν μας ενδιαφέρει καθολου
    if payload.message_id != 761204434670714912:
        return

    #αλλιώς ξέρουμε σε κάθε περίπτωση ότι είναι ακριβώς το μήνυμα που θέλουμε
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

    #ύστερα, βγάζουμε τον ρόλο σε αυτόν που έκανε το react με την φτιαχτή συνάρτησή μας
    await remove_role(reactor, role)

        

@client.event
async def on_message(message):
    #log του μηνύματος.
    print(message.author, "in", message.channel, "says:", message.content)

    #αν το μήνυμα είναι σε προσωπική συζήτηση, δεν χρειάζονται τα παρακάτω σε τίποτα.
    if (message.channel.type == discord.ChannelType.private):
        return

    server = client.get_guild(322050982747963392)

    #τα κανάλια του σέρβερ
    bot_requests      = server.get_channel(518904659461668868)
    geniki_sizitisi   = server.get_channel(518905389811630087)
    acquire_role      = server.get_channel(760736083544637511)
    secret_santa      = server.get_channel(787998456131354625)

    #οι ρόλοι που αναπαρίστανται στον σέρβερ
    metzi_tou_neoukti = server.get_role(488730147894198273)
    pcmci             = server.get_role(488730461091135488)
    me_meson          = server.get_role(654344275412385793)

    #οι admin
    GeorgeMC2610      = client.get_user(250721113729007617)
    Sotiris168        = await server.fetch_member(250973577761783808)

    #και όλοι οι συμμετέχοντες
    all_members = await server.fetch_members().flatten()

    #Μετατρέπουμε κάθε μήνυμα σε πεζά γράμματα.
    message.content = message.content.lower()
    respondable_messages = ["!ping", "!help", "-p", "-play", "-s", "-skip", "-ping", "-leave", "-l", "-help"]
    admin_commands = ["!display users", "!secret santa"]

    #                    ------ OI ENTOLES -------

    #Σιγουρευόμαστε ότι το BOT δεν θα απαντήσει ποτέ στον εαυτό του.
    if message.author == client.user:
        return

    #                                                                   Εκτέλεση εντολών διαχειριστών
    if message.content not in respondable_messages and message.content in admin_commands:
        #Ελέγχουμε αν όντως ο διαχειριστής εκτελεί εντολές.
        if message.author != Sotiris168 and message.author != GeorgeMC2610:
            msg_to_send = "Καλή προσπάθεια, " + message.author.mention + "! Αυτή είναι εντολή διαχειριστή. Θα 'ταν κρίμα αν το μάθαιναν οι " + metzi_tou_neoukti.mention + "..."
            await message.channel.send(msg_to_send)
            return

        #Αν έχουμε φτάσει μέχρι και αυτό το σημείο, σημαίνει ότι μόνο διαχειριστές θα εκτελούν εντολές. Οπότε τις εκτελούμε.
        else:
            if message.content == admin_commands[0]:
                #φτιάξε μια λίστα με τα αναγνώσιμα ονόματα των μελών του σέρβερ
                all_member_names = []
                #βάλε τα ονόματα στη λίστα
                for member in all_members:
                    all_member_names.append(member.name)
                #στείλε το μήνυμα με όλα τα ονόματα στη λίστα
                all_member_names.sort()
                await message.channel.send(all_member_names)
                return

            elif message.content == admin_commands[1]:
                #με αυτόν τον χρονοβόρο τρόπο, παίρνουμε το μήνυμα και το reaction στο οποίο θα δουλέψει το secret santa
                nickzouk = client.get_user(155441474861924355)
                provatas = client.get_user(172499322259243009)
                aimilios = client.get_user(206905752613421056)
                fotis    = client.get_user(232563110790168576)
                lefteris = client.get_user(371263663748939779)
                xanthos  = client.get_user(665585845167718426)
                aggelos  = client.get_user(476839396293738506)
                jason    = client.get_user(693124188785082399)
                vassilis = client.get_user(377389900338823188)

                #ύστερα, αυτή είναι η λίστα με την οποία θα δουλέψει το secret santa
                not_me_meson_members = []
                not_me_meson_members.append(fotis)
                not_me_meson_members.append(aimilios)
                not_me_meson_members.append(GeorgeMC2610)
                not_me_meson_members.append(Sotiris168)
                not_me_meson_members.append(lefteris)
                not_me_meson_members.append(aggelos)
                not_me_meson_members.append(xanthos)
                not_me_meson_members.append(nickzouk)
                not_me_meson_members.append(vassilis)
                
                #φτιάξε μια ακριβώς ίδια λίστα με την προηγούμενη, αλλά ανακάτεψέ την (για να είναι τυχαίος ο secret santa)
                secret_santas = not_me_meson_members.copy()
                random.shuffle(secret_santas)

                i = 0
                while (i < len(not_me_meson_members)):
                    duplicate = (not_me_meson_members[i] == nickzouk and secret_santas[i] == xanthos) or (not_me_meson_members[i] == aimilios and secret_santas[i] == nickzouk) or (not_me_meson_members[i] == xanthos and secret_santas[i] == lefteris) or (not_me_meson_members[i] == GeorgeMC2610 and secret_santas[i] == fotis) or (not_me_meson_members[i] == Sotiris168 and secret_santas[i] == aimilios)
                    if (not_me_meson_members[i] == secret_santas[i]) or duplicate:
                        random.shuffle(secret_santas)
                        i = 0
                    else:
                        i += 1

                i = 0
                #στείλε μήνυμα σε αυτόν που πρέπει και αποκάλυψέ του σε ποιόν πρέπει να κάνει δώρο
                for member in not_me_meson_members:
                    try:
                        user_msg_to_send = "**Δεν είσαι, πλέον,** ο secret santa του προηγούμενου.\nΕίσαι ο __**καινούργιος**__ secret santa του " + secret_santas[i].name + "."
                        await member.send(user_msg_to_send)
                    except Exception as e:
                        print("unable to send message to user", member, ". Exception:", e)
                    
                    i += 1
                return
    # ξεχωριστή περίπτωση για το prune
    elif message.content.startswith("!prune"):

        #Κι αυτή είναι εντολή διαχειριστή, οπότε θέλουμε κι αυτή να αποκαλύπτει τον παραβιαστή της
        if message.author.top_role != metzi_tou_neoukti:
            msg_to_send = "Καλή προσπάθεια, " + message.author.mention + "! Αυτή είναι εντολή διαχειριστή. Θα 'ταν κρίμα αν το μάθαιναν οι " + metzi_tou_neoukti.mention + "..."
            await message.channel.send(msg_to_send)
            return

        #χωρίζουμε το μήνυμα ανά κενό, ώστε να πάρουμε τις φορές που πρέπει να σβήσουμε το μήνυμα.
        message_content_by_space = message.content.split(" ")

        #πρέπει να 'χει ακριβώς ένα όρισμα το prune, αλλιώς δεν θα εκτελσθεί η εντολή.
        if len(message_content_by_space) != 2:
            await message.channel.send("ΣΤΕΙΛΕ ΣΩΣΤΑ ΤΗΝ ΕΝΤΟΛΗ, ΡΕ ΒΛΑΚΑ. \n\n`σωστός χειρισμός: !prune <αριθμός μηνυμάτων για σβήσιμο>`")
            return
        
        #ελέγχουμε αν είναι ακέραιος η τιμή που έστειλε
        try:
            times = int(message_content_by_space[1])

            #δεν πρέπει να 'ναι παραπάνω από πενήντα τα μηνύματα που θα σβησθούν.
            if times > 50 or times < 0:
                await message.channel.send("Τι λέτε, κύριε; ΜΑΞ ΠΕΝΗΝΤΑ ΛΕΞΕΙΣ, ΚΑΙ ΠΟΛΛΕΣ ΕΙΝΑΙ.")
                return

            #αλλιώς, δεν υπάρχει κανένα πρόβλημα και σβήνουμε τα μηνύματα.
            async for message_to_be_deleted in message.channel.history(limit=times):
                await message_to_be_deleted.delete()
            return
        except:
            await message.channel.send("Ε, καλά, είσαι και πολύ **μαλάκας**. ΑΡΙΘΜΟ ΔΩΣΕ, ΡΕ ΠΟΥΣΤΑΡΕ. \n\n`σωστός χειρισμός: !prune <αριθμός μηνυμάτων για σβήσιμο>`")
            return
                
  
    #                                                                  Εκτέλεση εντολών κοινής χρήσης
    if message.content in respondable_messages and message.content not in admin_commands:

        #Στην αρχή βλέπουμε αν το μήνυμα που εστάλη είναι στα bot requests. Αν δεν είναι, δεν εκτελείται η εντολή, σβήνεται η εντολή που εστάλη παράλληλα με το μήνυμα της ειδοποίησης με παράταση 5 δευτερολέπτων.
        if message.channel != bot_requests:

            #Λίστα μηνυμάτων απόρριψης
            deny1 = "Ξέρεις κάτι; **Όχι**, δεν θα κάνω αυτό που θες... τι το 'χουμε το " + bot_requests.mention + " ΒΡΕ ΜΑΛΑΚΑ; Αν θες πραγματικά να κάνω αυτό που θες, στείλ' το εκεί."
            deny2 = "Σου 'χω πει την ιστορία, όπου ένας άνθρωπος στέλνει τις εντολές του **ΟΝΤΩΣ** στο" + bot_requests.mention + ";"
            deny3 = "Κάθε φορά που στέλενεις εντολή έξω από το" + bot_requests.mention + " ένα κουταβάκι πεθαίνει... 😥"
            deny4 = "Γράψε 100 φορές στο τετράδιο σου 'ΘΑ ΣΤΕΛΝΩ ΤΙΣ ΕΝΤΟΛΕΣ ΜΟΥ ΜΟΝΟ ΣΤΟ " + bot_requests.mention + "'." 
            deny5 = "Στείλ' το στο " + bot_requests.mention + ", αλλιώς θα το πω στην κυρίααα 😨."
            deny6 = "🤡  <-- εσύ, όταν δεν στέλενεις τις εντολές σου στο " + bot_requests.mention + "."
            deny7 = "Θα έβαζες ποτέ το ψυγείο στο μπαλκόνι; Όχι. Μην βάζεις εντολές **έξω** του " + bot_requests.mention + ", τότε **__ΒΛΑΚΑ__**."
            deny8 = "Έχω πει 500 135.000 φορές να τα στέλνεις στο " + bot_requests.mention + "..."

            denying_messages = [deny1, deny2, deny3, deny4, deny5, deny6, deny7, deny8]

            #επιλέγουμε ένα τυχαίο από αυτά
            random_selection = random.randint(0, len(denying_messages)-1)

            #σβήνουμε το μήνυμα του χρήστη, και μετά αυτό που στέλενει το bot
            await message.delete()
            await message.channel.send(denying_messages[random_selection], delete_after=8.0) 
            return
        
        #Εκτέλεση των εντολών
        if message.content == respondable_messages[0]:
            await message.channel.send("Pong!")
            return

        if message.content == respondable_messages[1]:
            help_message = "**ΔΙΚΕΣ ΜΟΥ ΕΝΤΟΛΕΣ:** \n `!help` --> Δείχνει το παρόν μενού.\n `!ping` --> ανταπόκριση του μποτ με 'Pong!'.\n\n **ΕΝΤΟΛΕΣ ΔΙΑΧΕΙΡΙΣΤΗ:**\n `!display users` --> Προβολή όλων των μελών του σέρβερ.\n `!prune <αριθμός 1-50>` --> Σβήσιμο όλων των προηγούμενων μηνυμάτων\n `!secret santa` --> Νέα κλήρωση για secret santa."
            await message.channel.send(help_message)
            return
            
    #                                               Εδώ ελέγχουμε αν έχει σταλεί κάποιο μήνυμα σε library χωρίς φωτογραφία
    if message.channel.category_id == 749958245203836939:
        if not message.attachments:
            deny1 = "Σσσσσσσσσσσσσσσσσσσσσς! ***ΨΥΘΙΡΣΤΑ*** εδώ είναι βιβλιοθήκη! Δεν κάνει να μιλάμε εδώ..."
            deny2 = "Ρε κλόουν. Όχι μηνύματα εδώ. ΜΟΝΟ ΦΩΤΟΓΡΑΦΙΕΣ/ΒΙΝΤΕΟ."
            deny3 = "🚓 ΣΥΛΛΑΜΒΑΝΕΣΑΙ, ΒΛΑΚΑΚΟ. ΜΙΛΟΥΣΕΣ ΣΤΗ ΒΙΒΛΙΟΘΗΚΗ. 10 μέρες φυλακή μέχρι να μάθεις να στέλνεις μόνο φωτογραφίες ή βίντεο."
            deny4 = "Εδώ. Φωτογραφίες/Βίντεο. ***__ΜΟΝΟ__***. Εχμ, ωραία :)"

            denying_messages = [deny1, deny2, deny3, deny4]

            random_selection = random.randint(0, len(denying_messages)-1)
            await message.delete()
            await message.channel.send(denying_messages[random_selection], delete_after=8.0)
            return

client.run(token)