import discord
import random
import datetime
import requests
import json
from discord.ext import commands, tasks

#Εφ' όσον το repository θέλουμε να 'ναι public, πρέπει να αποθηκεύσουμε το token σε ένα ξεχωριστό αρχείο, το οποίο δεν θα συμπεριληφθεί στο repository.
f = open('token.txt', 'r')
token = f.read()
f.close()

f = open('emvolioapi.txt', 'r')
emvolioapi = f.read()
f.close()

client = discord.Client()

tonismena_grammata = ""

def channel_log(message):
    f = open('log.txt', 'a', encoding='utf-8')
    f.write("[" + str(datetime.datetime.now())[:19] + "]: " + message + "\n")
    print("[" + str(datetime.datetime.now())[:19] + "]: " + message)
    f.close()
    

#συναρτήσεις που ευθύνονται για τους ρόλους
async def give_role(member, role):
    if member is not None and role is not None:
        await member.add_roles(role)
        channel_log("Successfully gave role " + role.name + " to member " + member.name)

async def remove_role(member, role):
    if member is not None and role is not None:
        await member.remove_roles(role)
        channel_log("Successfully removed role " + role.name + " from member " + member.name)

#η συνάρτηση που αναγνωρίζει την θέση του μέμπερ
def identify_member_position(member):
    server = client.get_guild(322050982747963392)
    
    metzi_tou_neoukti = server.get_role(488730147894198273)
    if member.top_role == metzi_tou_neoukti:
        return 4
    
    bots = server.get_role(456219306468966410)
    if member.top_role == bots:
        return 3

    pcmci = server.get_role(488730461091135488)
    if member.top_role == pcmci:
        return 2

    me_meson          = server.get_role(654344275412385793)
    if member.top_role == me_meson:
        return 1
    
    return 0

async def private_msg(message, sender):
    if '{' in message and message[-1] == '}' and '"target"' in message and '"message"' in message:
        payload  = json.loads(message.split("send ")[1])
        targetID = False

        server   = client.get_guild(322050982747963392)
        users    = await server.fetch_members().flatten()

        try:
            targetID = [i for i in users if i.name == payload["target"]][0].id
            await sender.send("Θα στείλω στον " + payload["target"] + " **αμέσως**!")
        except Exception as e:
            print("Unable to decode dictionary.", e.args)
            await sender.send("Ποιός στον πούτσο είναι αυτός;")
        
        if targetID:
            user_to_send = client.get_user(targetID)
            await user_to_send.send(payload["message"])
            await sender.send("Και, που λες, του το έστειλα.")



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

    #ύστερα, βγάζουμε τον ρόλο σε αυτόν που έκανε το react με την φτιαχτή συνάρτησή μας
    await remove_role(reactor, role)

@client.event
async def on_message(message):
    #log του μηνύματος.
    channel_log(message.author.name + " in " + str(message.channel) + " says: " + message.content)

    if message.author == client.user:
        return

    server = client.get_guild(322050982747963392)

    #τα κανάλια του σέρβερ
    bot_requests      = server.get_channel(518904659461668868)
    geniki_sizitisi   = server.get_channel(518905389811630087)
    acquire_role      = server.get_channel(760736083544637511)
    secret_santa      = server.get_channel(787998456131354625)

    #οι ρόλοι που αναπαρίστανται στον σέρβερ
    metzi_tou_neoukti = server.get_role(488730147894198273)

    #οι admin
    GeorgeMC2610      = await server.fetch_member(250721113729007617)
    Sotiris168        = await server.fetch_member(250973577761783808)

    #αν το μήνυμα είναι σε προσωπική συζήτηση, δεν χρειάζονται τα παρακάτω σε τίποτα. Επίσης σιγουρευόμαστε ότι το bot δεν θα απαντάει ποτέ στον εαυτό του.
    if message.channel.type == discord.ChannelType.private:
        if message.content.startswith("send "):
            if message.author != GeorgeMC2610:
                await message.author.send("ΤΙ ΠΑΣ ΝΑ ΚΑΝΕΙΣ ΕΚΕΙ;")
                await GeorgeMC2610.send("ΓΙΑ ΒΑΛΕ ΜΙΑ ΤΑΞΗ. Ο " + message.author.name + " ΚΑΝΕΙ ΤΣΑΤΣΙΕΣ.")
                return

            await private_msg(message.content, message.author)
            return
        
        return
    

    #Μετατρέπουμε κάθε μήνυμα σε πεζά γράμματα.
    message.content = message.content.lower()
    respondable_messages = ["!ping", "!help", "!emvolio", "!join", "!leave", "-", "!"]
    admin_commands = ["!display members", "!prune"]

    #Εκτέλεση εντολών διαχειριστών
    if [i for i in admin_commands if message.content.startswith(i)] != []:
        #Ελέγχουμε αν όντως ο διαχειριστής εκτελεί εντολές.
        if identify_member_position(message.author) != 4:
            msg_to_send = "Καλή προσπάθεια, " + message.author.mention + "! Αυτή είναι εντολή διαχειριστή. Θα 'ταν κρίμα αν το μάθαιναν οι " + metzi_tou_neoukti.mention + "..."
            await message.channel.send(msg_to_send)
            return

        if message.content == admin_commands[0]:
            #και όλοι οι συμμετέχοντες
            all_members      = await server.fetch_members().flatten()
            all_member_names = [i.name for i in all_members]

            #κάνουμε και καταμέτρηση των bot
            bots             = [i for i in all_members if identify_member_position(i) == 3]

            #στείλε το μήνυμα με όλα τα ονόματα στη λίστα
            all_member_names.sort()
            await message.channel.send("```python\n" + str(all_member_names) + "``` **\n" + str(len(all_member_names)) + " συνολικά μέλη** στον server, όπου τα **" + str(len(bots)) + " είναι bots.**")
            return

        elif message.content.startswith(admin_commands[1]):
            #χωρίζουμε το μήνυμα ανά κενό, ώστε να πάρουμε τις φορές που πρέπει να σβήσουμε το μήνυμα.
            message_content_by_space = message.content.split(" ")

            #πρέπει να 'χει ακριβώς ένα όρισμα το prune, αλλιώς δεν θα εκτελσθεί η εντολή.
            if len(message_content_by_space) != 2:
                await message.channel.send("ΣΤΕΙΛΕ ΣΩΣΤΑ ΤΗΝ ΕΝΤΟΛΗ, ΡΕ ΒΛΑΚΑ. \n\n**σωστός χειρισμός:** `!prune <αριθμός μηνυμάτων (από 1-50) για σβήσιμο>`")
                return
            
            #ελέγχουμε αν είναι ακέραιος η τιμή που έστειλε
            try:
                times = int(message_content_by_space[1])

                #δεν πρέπει να 'ναι παραπάνω από πενήντα τα μηνύματα που θα σβησθούν.
                if times > 50:
                    await message.channel.send("Τι λέτε, κύριε; ΜΑΞ ΠΕΝΗΝΤΑ MHNYMATA. ΚΑΙ ΠΟΛΛA ΕΙΝΑΙ ΜΗ ΣΟΥ ΠΩ.")
                    return
                elif times < 0:
                    await message.channel.send("Και για πες, ρε βλάκα, ΠΩΣ ΘΑ ΣΒΗΣΩ **ΑΡΝΗΤΙΚΟ** ΑΡΙΘΜΟ ΜΗΝΥΜΑΤΩΝ;")
                    return

                #αλλιώς, δεν υπάρχει κανένα πρόβλημα και σβήνουμε τα μηνύματα.
                await message.delete()
                async for message_to_be_deleted in message.channel.history(limit=times):
                    await message_to_be_deleted.delete()
                return
            except:
                await message.channel.send("Ε, καλά, είσαι και πολύ **μαλάκας**. ΑΡΙΘΜΟ ΔΩΣΕ, ΡΕ ΠΟΥΣΤΑΡΕ. \n\n**σωστός χειρισμός:** `!prune <αριθμός μηνυμάτων (από 1-50) για σβήσιμο>`")
                return
                
    #Εκτέλεση εντολών κοινής χρήσης
    if [i for i in respondable_messages if message.content.startswith(i)] != []:

        #αν κάποιος χρήστης έχει στείλει απλά μια πάυλα στην αρχή, τότε δεν χρειάζεται να κάνουμε κάτι
        if message.content[0] == "-" and message.content[-1] == "-":
            return
        
        #Στην αρχή βλέπουμε αν το μήνυμα που εστάλη είναι στα bot requests. Αν δεν είναι, δεν εκτελείται η εντολή, σβήνεται η εντολή που εστάλη παράλληλα με το μήνυμα της ειδοποίησης με παράταση 5 δευτερολέπτων.
        if message.channel != bot_requests:

            #Λίστα μηνυμάτων απόρριψης
            deny1 = "Ξέρεις κάτι; **Όχι**, δεν θα κάνω αυτό που θες... τι το 'χουμε το " + bot_requests.mention + " ΒΡΕ ΜΑΛΑΚΑ; Αν θες πραγματικά να γίνει αυτό που θες, στείλ' το εκεί."
            deny2 = "Σου 'χω πει την ιστορία, όπου ένας άνθρωπος στέλνει τις εντολές του **ΟΝΤΩΣ** στο" + bot_requests.mention + ";"
            deny3 = "Κάθε φορά που στέλενεις εντολή έξω από το" + bot_requests.mention + " ένα κουταβάκι πεθαίνει... 😥"
            deny4 = "Γράψε 100 φορές στο τετράδιο σου 'ΘΑ ΣΤΕΛΝΩ ΤΙΣ ΕΝΤΟΛΕΣ ΜΟΥ ΜΟΝΟ ΣΤΟ " + bot_requests.mention + "'." 
            deny5 = "Στείλ' το στο " + bot_requests.mention + ", αλλιώς θα το πω στην κυρίααα 😨."
            deny6 = "🤡  ← εσύ, όταν δεν στέλνεις τις εντολές σου στο " + bot_requests.mention + "."
            deny7 = "Θα έβαζες ποτέ το ψυγείο στο μπαλκόνι; Όχι. Μην βάζεις εντολές **έξω** του " + bot_requests.mention + ", τότε **__ΒΛΑΚΑ__**."
            deny8 = "Έχω πει 500 135.000 φορές να τα στέλνεις στο " + bot_requests.mention + "..."
            deny9 = "🚓🚓 **ΑΣΤΥΝΟΜΙΑ ΒΛΑΚΕΙΑΣ!** Ήμουν σίγουρος, ότι κάποιος σαν κι εσένα, θα έστελνε εντολή εκτός του " + bot_requests.mention + "!"

            denying_messages = [deny1, deny2, deny3, deny4, deny5, deny6, deny7, deny8, deny9]

            #επιλέγουμε ένα τυχαίο από αυτά
            random_deny_message = random.choice(denying_messages)

            #σβήνουμε το μήνυμα του χρήστη, και μετά αυτό που στέλενει το bot
            await message.delete()
            await message.channel.send(random_deny_message, delete_after=8.0) 
            return
        
        #Εκτέλεση των εντολών
        if message.content == respondable_messages[0]:
            await message.channel.send("Pong!")
            return

        if message.content == respondable_messages[1]:
            help_message = "**ΔΙΚΕΣ ΜΟΥ ΕΝΤΟΛΕΣ:** \n `!help` --> Δείχνει το παρόν μενού.\n `!ping` --> ανταπόκριση του μποτ με 'Pong!'.\n\n **ΕΝΤΟΛΕΣ ΔΙΑΧΕΙΡΙΣΤΗ:**\n `!display users` --> Προβολή όλων των μελών του σέρβερ.\n `!prune <αριθμός 1-50>` --> Σβήσιμο όλων των προηγούμενων μηνυμάτων"
            await message.channel.send(help_message)
            return

        if message.content.startswith(respondable_messages[2]):
            #για να βρούμε ποια πόλη θέλει ο χρήστης, πρώτα χωρίζουμε την εντολή και ύστερα την κάνουμε κεφαλαία, για το API
            city = message.content.split("!emvolio ")[1].upper()

            #κάνουμε την κατάληξη να 'ναι σήμερα εξ αρχής
            date = datetime.date.today()
            kataliksi = "σήμερα"
            
            #αλλά αν είναι πολύ νωρίς μέσα στην μέρα, βγάζουμε τα χθεσινά αποτελέσματα
            if datetime.datetime.now().hour < 17:
                date -= datetime.timedelta(days=1)
                kataliksi = "χθες"

            #φτιάχνουμε το request και παίρνουμε τα γεγονότα όπως πρέπει
            url = 'https://data.gov.gr/api/v1/query/mdg_emvolio?date_from=' + str(date) + '&date_to=' + str(date)
            headers = {'Authorization':'Token ' + emvolioapi}
            response = requests.get(url, headers=headers)
            response = response.json()
            
            #αν για οποιονδήποτε λόγο δεν έχουμε αποτελέσματα, τότε σταματάμε εδώ
            if response == []:
                await message.channel.send("Δεν έχουν γίνει ακόμη εμβολιασμοί σήμερα.")
                return

            #αλλιώς προσπαθούμε να βρούμε την περιοχή
            try:
                #εκτός αν ο χρήστης μας έχει πει να βρούμε όλες τις περιοχές
                if city == "ΣΥΝΟΛΟ":
                    #στην οποία περίπτωση κάνουμε κάτι τέτοιο χειροκίνητα
                    grand_total = 0
                    grand_today_total = 0
                    for data in response:
                        grand_total += data["totalvaccinations"]
                        grand_today_total += data["daytotal"]

                    await message.channel.send('Έχουν γίνει συνολικά **' + str(grand_total) + ' εμβολιασμοί** σε ολόκληρη την Ελλάδα. (' + str(grand_today_total) + ' έγιναν ' + kataliksi + ')')
                    return

                #βρίσκουμε την περιοχή με LINQ-οειδές request
                total_vaccines = [data for data in response if data["area"] == city][0]
                #και στέλνουμε το μήνυμα
                await message.channel.send('Στην περιφερειακή ενότητα **' + city + '** έχουν γίνει συνολικά **' + str(total_vaccines["totalvaccinations"]) + ' εμβολιασμοί**. (' + str(total_vaccines["daytotal"]) + ' έγιναν ' + kataliksi + ')')
            except:
                #αλλιώς, λογικά δεν θα υπάρχει αυτή η περιοχή
                await message.channel.send('Δεν βρήκα αυτήν την περιφερειακή ενότητα. 😫 (Η περιοχή που ψάχνεις πρέπει να είναι υποχρεωτικά σε __γενική πτώση__)')

            return
            
    #Εδώ ελέγχουμε αν έχει σταλεί κάποιο μήνυμα σε library χωρίς φωτογραφία
    if message.channel.category_id == 749958245203836939 and not message.attachments:
        deny1 = "Σσσσσσσσσσσσσσσσσσσσσς! ***ΨΥΘΙΡΣΤΑ*** εδώ είναι βιβλιοθήκη! Δεν κάνει να μιλάμε εδώ..."
        deny2 = "Ρε κλόουν. Όχι μηνύματα εδώ. ΜΟΝΟ ΦΩΤΟΓΡΑΦΙΕΣ/ΒΙΝΤΕΟ."
        deny3 = "🚓 ΣΥΛΛΑΜΒΑΝΕΣΑΙ, ΒΛΑΚΑΚΟ. ΜΙΛΟΥΣΕΣ ΣΤΗ ΒΙΒΛΙΟΘΗΚΗ. 10 μέρες φυλακή μέχρι να μάθεις να στέλνεις μόνο φωτογραφίες ή βίντεο."
        deny4 = "Εδώ. Φωτογραφίες/Βίντεο. ***__ΜΟΝΟ__***. Εχμ, ωραία :)"

        denying_messages = [deny1, deny2, deny3, deny4]

        random_deny_message = random.choice(denying_messages)
        await message.delete()
        await message.channel.send(random_deny_message, delete_after=8.0)
        return

    #Το bot πλέον απαντάει όταν το κάνει mention κάποιος.
    if "<@!640605837102022696>" in message.content:
        plaint1 = "Τιιιιι;"
        plaint2 = "ΤΙ ΘΕΕΕΕΣ;"
        plaint3 = "Τι έκανα πάλι;"
        plaint4 = "ΣΚΑΣΕΕΕΕΕ."
        plaint5 = "Άλλη μία φορά να το πεις αυτό και θα σε διώξω."
        plaint6 = GeorgeMC2610.mention + " ΚΑΝΕΕΕΕ ΚΑΤΙΙΙ ΜΕ ΕΝΟΧΛΟΥΝ."
        plaint7 = "Πω, ρε μαλάκα αλήθεια σκάσε..."

        complaints = [plaint1, plaint2, plaint3, plaint4, plaint5, plaint6, plaint7]
        random_complaint = random.choice(complaints)
        await message.channel.send(random_complaint)

    if "nibbaebi" in message.content.lower():
        await message.delete()
        await message.author.move_to(None)
        channel_log("Attempted to disconnect " + message.author.name + " from a voice channel (Nibbaebi.)")
        await message.channel.send("Give this mothafucka a 27 minute ban for being toxic, I'm French. (Κατουράω το Miliobot)")
        
client.run(token)