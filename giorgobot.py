import discord
import random
import datetime
import requests
import json
import locale
import flag

#Εφ' όσον το repository θέλουμε να 'ναι public, πρέπει να αποθηκεύσουμε το token σε ένα ξεχωριστό αρχείο, το οποίο δεν θα συμπεριληφθεί στο repository.
f = open('token.txt', 'r')
token = f.read()
f.close()

f = open('emvolioapi.txt', 'r')
emvolioapi = f.read()
f.close()

client = discord.Client()

#μηνύματα για την προβολή του !help
help_dialog1 = '**ΔΙΚΕΣ ΜΟΥ ΕΝΤΟΛΕΣ:**'
help_dialog2 = '`giorg help` → Δείχνει το παρόν μενού.'
help_dialog3 = '`giorg ping` → Ανταπόκριση του μποτ με "Pong!"'
help_dialog4 = '`giorg emvolio <όνομα περιφερειακής ενότητας>` → Προβολή των συνολικών και ημερίσιων εμβολιασμών της περιφερειακής ενότητας.'
help_dialog5 = '`giorg emvolio <σύνολο|όλα|όλο|Ελλάδα|χώρα|συνολικά|πάντες>` → Προβολή των συνολικών και ημερίσιων εμβολιασμών όλης της Ελλάδας.'
help_dialog6 = '`giorg emvolio <περιφέρειες|περιφερειακές ενότητες|λίστα|ενότητες|περιοχές>` → Προβολή των διαθέσιμων περιοχών, για την ανάκτηση δεδομένων του εμβολίου.'
help_dialog7 = '`giorg corona <χώρα στα αγγλικά>` → Προβολή συνολικών και ημερισίων κρουσμάτων και θανάτων από την COVID-19 της επιλεγμένης χώρας.'
help_dialog8 = '`giorg corona <list|all|countries>` → Προβολή των διαθέσιμων χωρών, για ανάκτηση στατιστικών στοιχείων περί COVID-19 (κρούσματα & θάνατοι).'
help_dialog9 = '**ΕΝΤΟΛΕΣ ΔΙΑΧΕΙΡΙΣΤΗ:**'
help_dialog95 = '`giorg display members` → Προβολή όλων των μελών του σέρβερ.' 
help_dialog96 = '`giorg prune <αριθμός 1-50>` → Σβήσιμο όλων των προηγούμενων μηνυμάτων"'
help_dialog97 = '`giorg announcegeniki <μήνυμα>` → Άμεση αποστολή μηνύματος, από εμένα, στο κανάλι <#518905389811630087>'
help_dialog98 = '`giorg announcebot <μήνυμα>` → Άμεση αποστολή μηνύματος, από εμένα, στο κανάλι <#518904659461668868>'
help_dialog99 = '`giorg announce {"channel":"<ακριβές όνομα καναλιού>", "message":"<μήνυμα>"}` → Άμεση αποστολή μηνύματος, από εμένα, σε συγκεκριμένο κανάλι που ορίζεται στο πεδίο `channel`.'

help_message = help_dialog1 + '\n' + help_dialog2 + '\n' + help_dialog3 + '\n' + help_dialog4 + '\n' + help_dialog5 + '\n' + help_dialog6 + '\n' +  help_dialog7 + '\n' + help_dialog8 + '\n\n' + help_dialog9 + '\n' + help_dialog95  + '\n' + help_dialog96 + '\n' + help_dialog97  + '\n' + help_dialog98 + '\n' + help_dialog99

#Λίστα μηνυμάτων απόρριψης
deny1 = "Ξέρεις κάτι; **Όχι**, δεν θα κάνω αυτό που θες... τι το 'χουμε το " + '<#518904659461668868>' + " ΒΡΕ ΜΑΛΑΚΑ; Αν θες πραγματικά να γίνει αυτό που θες, στείλ' το εκεί."
deny2 = "Σου 'χω πει την ιστορία, όπου ένας άνθρωπος στέλνει τις εντολές του **ΟΝΤΩΣ** στο " + '<#518904659461668868>' + ";"
deny3 = "Κάθε φορά που στέλενεις εντολή έξω από το" + '<#518904659461668868>' + " ένα κουταβάκι πεθαίνει... 😥"
deny4 = "Γράψε 100 φορές στο τετράδιο σου 'ΘΑ ΣΤΕΛΝΩ ΤΙΣ ΕΝΤΟΛΕΣ ΜΟΥ ΜΟΝΟ ΣΤΟ " + '<#518904659461668868>' + "'." 
deny5 = "Στείλ' το στο " + '<#518904659461668868>' + ", αλλιώς θα το πω στην κυρίααα 😨."
deny6 = "🤡  ← εσύ, όταν δεν στέλνεις τις εντολές σου στο " + '<#518904659461668868>' + "."
deny7 = "Θα έβαζες ποτέ το ψυγείο στο μπαλκόνι; Όχι. Μην βάζεις εντολές **έξω** του " + '<#518904659461668868>' + ", τότε **__ΒΛΑΚΑ__**."
deny8 = "Έχω πει 500 135.000 φορές να τα στέλνεις στο " + '<#518904659461668868>' + "..."
deny9 = "🚓🚓 **ΑΣΤΥΝΟΜΙΑ ΒΛΑΚΕΙΑΣ!** Ήμουν σίγουρος, ότι κάποιος σαν κι εσένα, θα έστελνε εντολή εκτός του " + '<#518904659461668868>' + "!"

denying_messages = [deny1, deny2, deny3, deny4, deny5, deny6, deny7, deny8, deny9]

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

#Εντολής απόρριψης εντολής
pm_deny1 = "Απλά άσ' το. ΔΕΝ ΤΟ 'ΧΕΙΣ."
pm_deny2 = "Μην είσαι σίγουρος ότι δεν θα το μάθει ο GeorgeMC2610."
pm_deny3 = "ΧΑΧΑΧΑΧΑΧΑΧΑΧΑΝΑΙΚΑΛΑ"

pm_denying = [pm_deny1, pm_deny2, pm_deny3]


respondable_messages = ["giorg ping", "giorg help", "giorg emvolio", "giorg corona", "-", "!", "r6s"]
admin_commands       = ["giorg display members", "giorg prune", "giorg announcegeniki", "giorg announcebot", "giorg announce"]


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

#η συνάρτηση που αναγνωρίζει την θέση του μέμπερ
def identify_member_position(member):
    server = client.get_guild(322050982747963392)
    
    metzi_tou_neoukti = server.get_role(488730147894198273)
    if member.top_role == metzi_tou_neoukti:
        return 5

    skase = server.get_role(821739015970619393)
    if member.top_role == skase:
        return 4

    bots = server.get_role(456219306468966410)
    if member.top_role == bots:
        return 3

    pcmci = server.get_role(456219306468966410)
    if member.top_role == pcmci:
        return 2

    me_meson = server.get_role(654344275412385793)
    if member.top_role == me_meson:
        return 1
    
    return 0

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
    print('Bot online.')

@client.event
async def on_message(message):
    #log του μηνύματος.
    channel_log(str(message.author) + " in " + str(message.channel) + " says: " + message.content)

    if message.author == client.user:
        return
    
    server = await client.fetch_guild(322050982747963392)

    #αν το μήνυμα είναι σε προσωπική συζήτηση, δεν χρειάζονται τα παρακάτω σε τίποτα. Επίσης σιγουρευόμαστε ότι το bot δεν θα απαντάει ποτέ στον εαυτό του.
    if message.channel.type == discord.ChannelType.private:
        if (str(message.author) != "GeorgeMC2610#8036" and str(message.author) != "Sotiris168#5790") and ([i for i in admin_commands if message.content.startswith(i)] != []):
            GeorgeMC2610 = await client.fetch_user(250721113729007617)
            await message.author.send(random.choice(pm_denying))
            await GeorgeMC2610.send("Ο γνωστός άγνωστος " + message.author.name + " προσπάθησε ΝΑ ΜΕ ΚΑΝΕΙ ΝΑ ΚΑΝΩ ΚΑΤΙ ΠΟΥ ΔΕΝ ΠΡΕΠΕΙ.")
            return
        
        if message.content.startswith("!send "):
            await private_msg(message.content, message.author)
            return
        
        elif message.content.startswith(admin_commands[2]):
            try:
                geniki_sizitisi = await client.fetch_channel(518905389811630087)
                await geniki_sizitisi.send(message.content.split("!announcegeniki ")[1])
                await message.author.send("Όλα οκ, μαν. Το 'στειλα στην **γενική συζήτηση**.")
            except Exception as ex:
                await message.author.send("ΩΠΑ, ΚΑΤΣΕ, ΚΑΤΙ ΔΕΝ Μ' ΑΡΕΣΕΙ ΕΔΩ. " + ex.args)
            return
        
        elif message.content.startswith(admin_commands[3]):
            try:
                bot_requests = await client.fetch_channel(518904659461668868)
                await bot_requests.send(message.content.split("!announcebot ")[1])
                await message.author.send("Όλα οκ, μαν. Το 'στειλα στα **bot requests**.")
            except Exception as ex:
                await message.author.send("ΩΠΑ, ΚΑΤΣΕ, ΚΑΤΙ ΔΕΝ Μ' ΑΡΕΣΕΙ ΕΔΩ. " + ex.args)
            return

        elif message.content.startswith(admin_commands[4]):
            await announce(message.content, message.author)
            return

        return 

    #Μετατρέπουμε κάθε μήνυμα σε πεζά γράμματα.
    message.content = message.content.lower()

    #Εκτέλεση εντολών διαχειριστών
    if [i for i in admin_commands if message.content.startswith(i)] != []:
        #Ελέγχουμε αν όντως ο διαχειριστής εκτελεί εντολές.
        if identify_member_position(message.author) < 4:
            msg_to_send = "Καλή προσπάθεια, " + message.author.mention + "! Αυτή είναι εντολή διαχειριστή. Θα 'ταν κρίμα αν το μάθαιναν οι <@&488730147894198273>, <@&821739015970619393>..."
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
            message_content_by_space = message.content.split("giorg prune ")

            #πρέπει να 'χει ακριβώς ένα όρισμα το prune, αλλιώς δεν θα εκτελσθεί η εντολή.
            if len(message_content_by_space) != 2:
                await message.channel.send("ΣΤΕΙΛΕ ΣΩΣΤΑ ΤΗΝ ΕΝΤΟΛΗ, ΡΕ ΒΛΑΚΑ. \n\n**σωστός χειρισμός:** `!prune <αριθμός μηνυμάτων (από 1-50) για σβήσιμο>`")
                return
            
            #ελέγχουμε αν είναι ακέραιος η τιμή που έστειλε
            try:
                times = int(message_content_by_space[1])

                #δεν πρέπει να 'ναι παραπάνω από πενήντα τα μηνύματα που θα σβησθούν.
                if times == 69420:
                    await message.channel.send("Ναι ναι ναι, ΧΑ-ΧΑ. Μαλάκα, ε μαλάκα.")
                    return
                elif times > 50:
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
        if message.channel.id != 518904659461668868:
            #επιλέγουμε ένα τυχαίο από αυτά
            random_deny_message = random.choice(denying_messages)

            #σβήνουμε το μήνυμα του χρήστη, και μετά αυτό που στέλενει το bot
            await message.delete()
            await message.channel.send(random_deny_message, delete_after=8.0) 
            return
        
        #Εκτέλεση των εντολών
        #giorg ping
        if message.content == respondable_messages[0]:
            await message.channel.send("Pong!")
            return

        #giorg help
        if message.content == respondable_messages[1]:
            await message.channel.send(help_message)
            return

        #giorg emvolio
        if message.content.startswith(respondable_messages[2]):
            #για να βρούμε ποια πόλη θέλει ο χρήστης, πρώτα χωρίζουμε την εντολή και ύστερα την κάνουμε κεφαλαία, για το API
            city = message.content.split("giorg emvolio ")[1].upper()
            city = remove_greek_uppercase_accent(city)

            #κάνουμε την κατάληξη να 'ναι σήμερα εξ αρχής
            date = datetime.date.today()
            kataliksi = 'σήμερα'
            
            #αλλά αν είναι πολύ νωρίς μέσα στην μέρα, βγάζουμε τα χθεσινά αποτελέσματα
            if datetime.datetime.now().hour < 20:
                date -= datetime.timedelta(days=1)
                kataliksi = 'χθες'

            #φτιάχνουμε το request και παίρνουμε τα γεγονότα όπως πρέπει
            url = 'https://data.gov.gr/api/v1/query/mdg_emvolio?date_from=' + str(date) + '&date_to=' + str(date)
            headers = {'Authorization':'Token ' + emvolioapi}
            response = requests.get(url, headers=headers)
            response = response.json()
            
            #αν για οποιονδήποτε λόγο δεν έχουμε αποτελέσματα, τότε σταματάμε εδώ
            if response == []:
                await message.channel.send("Δεν έχουν γίνει ακόμη εμβολιασμοί σήμερα.")
                return

            locale.setlocale(locale.LC_ALL, 'el_GR')

            #αλλιώς προσπαθούμε να βρούμε την περιοχή
            try:
                #εκτός αν ο χρήστης μας έχει πει να βρούμε όλες τις περιοχές
                if city in ["ΣΥΝΟΛΟ", "ΟΛΑ", "ΟΛΟ", "ΟΛΟΙ", "ΕΛΛΑΔΑ", "ΧΩΡΑ", "ΣΥΝΟΛΙΚΑ", "ΠΑΝΤΕΣ"]:
                    #στην οποία περίπτωση κάνουμε κάτι τέτοιο χειροκίνητα
                    grand_total = 0
                    grand_dose1_total = 0
                    grand_dose2_total = 0

                    grand_today_total = 0
                    grand_today_dose1_total = 0
                    grand_today_dose2_total = 0
                    for data in response:
                        grand_total += data["totalvaccinations"]
                        grand_dose1_total += data["totaldose1"]
                        grand_dose2_total += data["totaldose2"]

                        grand_today_total += data["daytotal"]
                        grand_today_dose1_total += data["dailydose1"]
                        grand_today_dose2_total += data["dailydose2"]

                    percentage = str(round(float(grand_dose2_total*100/8658460), 1)) + '%'
                    rythm      = str(round((8658460*0.7 - grand_dose2_total) / grand_today_dose2_total)) + ' μέρες'

                    embedded_message = discord.Embed(title=flag.flag('gr') + " ΣΥΝΟΛΙΚΟΙ ΕΜΒΟΛΙΑΣΜΟΙ", description="Αναλυτικοί εμβολιασμοί **__για " + kataliksi + "__**.")
                    embedded_message.set_thumbnail(url="https://www.gov.gr/gov_gr-thumb-1200.png")

                    embedded_message.add_field(name="Δόση 1️⃣", value='Έγιναν **' + f'{grand_today_dose1_total:n}' + '** εμβολιασμοί. (**' + f'{grand_dose1_total:n}' + '** σύνολο)', inline=True)
                    embedded_message.add_field(name="Δόση 2️⃣", value='Έγιναν **' + f'{grand_today_dose2_total:n}' + '** εμβολιασμοί. (**' + f'{grand_dose2_total:n}' + '** σύνολο)', inline=True)
                    embedded_message.add_field(name="Αθροιστικά 💉", value='Έγιναν **' + f'{grand_today_total:n}' + '** εμβολιασμοί. (**' + f'{grand_total:n}' + '** σύνολο).', inline=True)

                    embedded_message.add_field(name="Πληρότητα ✅", value="Το **" + percentage.replace('.', ',') + "** του **ενήλικου** πληθυσμού έχει __τελειώσει__ με τον εμβολιασμό.", inline=True)
                    embedded_message.add_field(name="Ρυθμός 🕖", value="Με τα δεδομένα " + kataliksi + ", σε **" + rythm + "** θα έχει εμβολιαστεί το 70% του **ενήλικου** πληθυσμού.", inline=True)

                    embedded_message.set_footer(text="Δεδομένα από το https://emvolio.gov.gr/")

                    await message.channel.send(embed=embedded_message)
                    return

                elif city in ["ΠΕΡΙΦΕΡΕΙΕΣ", "ΠΕΡΙΦΕΡΕΙΑΚΕΣ ΕΝΟΤΗΤΕΣ", "ΛΙΣΤΑ", "ΕΝΟΤΗΤΕΣ", "ΠΕΡΙΟΧΕΣ"]:
                    total_cities = [data["area"] for data in response]
                    await message.channel.send('```py\n ' + str(total_cities) + '```\n ● **' + str(len(total_cities)) + '** συνολικές περιφερειακές ενότητες.')

                    return

                #βρίσκουμε την περιοχή με LINQ-οειδές request
                total_vaccines = [data for data in response if data["area"] == city][0]

                #μαζεύουμε το μήνυμα σε embed
                embedded_message = discord.Embed(title='📍 ΠΕΡΙΦΕΡΕΙΑΚΗ ΕΝΟΤΗΤΑ ' + city, description="Αναλυτικοί εμβολιασμοί **__για " + kataliksi + "__**.")
                embedded_message.set_thumbnail(url="https://www.gov.gr/gov_gr-thumb-1200.png")

                embedded_message.add_field(name="Δόση 1️⃣", value='Έγιναν **' + f'{total_vaccines["dailydose1"]:n}' + '** εμβολιασμοί. (**' + f'{total_vaccines["totaldose1"]:n}' + '** σύνολο)', inline=True)
                embedded_message.add_field(name="Δόση 2️⃣", value='Έγιναν **' + f'{total_vaccines["dailydose2"]:n}' + '** εμβολιασμοί. (**' + f'{total_vaccines["totaldose2"]:n}' + '** σύνολο)', inline=True)
                embedded_message.add_field(name="Αθροιστικά 💉", value='Έγιναν **' + f'{total_vaccines["daytotal"]:n}' + '** εμβολιασμοί. (**' + f'{total_vaccines["totalvaccinations"]:n}' + '** σύνολο).', inline=False)

                embedded_message.set_footer(text="Δεδομένα από το https://emvolio.gov.gr/")

                #και στέλνουμε το μήνυμα
                await message.channel.send(embed=embedded_message)
            except Exception as e:
                #αλλιώς, λογικά δεν θα υπάρχει αυτή η περιοχή
                await message.channel.send('Δεν βρήκα αυτήν την περιφερειακή ενότητα. 😫 Δες τις διαθέσιμες περιοχές με την εντολή `giorg emvolio λίστα`.')
                print(e.args)
            
            return

        #giorg corona
        if message.content.startswith(respondable_messages[3]):
            country  = message.content.split("giorg corona ")[1]

            #κάνουμε την κατάληξη να 'ναι σήμερα εξ αρχής
            kataliksi = "σήμερα"
            yesterday = 'false'
            
            #αλλά αν είναι πολύ νωρίς μέσα στην μέρα, βγάζουμε τα χθεσινά αποτελέσματα
            if datetime.datetime.now().hour < 18:
                kataliksi = "χθες"
                yesterday = 'true'

            #φτιάχνουμε το request και παίρνουμε τα γεγονότα όπως πρέπει
            url = 'https://disease.sh/v3/covid-19/countries?yesterday=' + yesterday + '&twoDaysAgo=false&sort=cases&allowNull=false'
            response = requests.get(url)
            response = response.json()

            #αν ο χρήστης θέλει λίστα με όλες τις χώρες, δεν πηγαίνουμε παρακάτω, και απλά του τις προβάλλουμε
            if country.casefold() in ['List'.casefold(), 'ALL'.casefold(), 'Countries'.casefold()]:
                countries = [data["country"] for data in response]
                countries.sort()
                await message.channel.send('```python\n' + str(countries[:len(countries)//2]) + '```')
                await message.channel.send('```python\n' + str(countries[len(countries)//2:]) + '```\n ● **' + str(len(countries)) + '** συνολικές διαθέσιμες χώρες-κλειδιά.')
                return

            try:
                locale.setlocale(locale.LC_ALL, 'el_GR')
                country_info = ''

                #ανάλογα με το πόσα γράμματα είχε η χώρα που έβαλε ο χρήστης, ψάχνουμε και την ανάλογη χώρα
                if len(country) == 2:
                    country_info = [data for data in response if data["countryInfo"]["iso2"] == country.upper()].pop()
                elif len(country) == 3:
                    country_info = [data for data in response if data["countryInfo"]["iso3"] == country.upper()].pop()
                else:
                    country_info = [data for data in response if data["country"].casefold() == country.casefold()].pop()
                
                #ανακτάμε το εμότζι και το όνομα της χώρας για να το βάλουμε στο συγχωνευμένο μήνυμα
                country_emoji = flag.flag(country_info["countryInfo"]["iso2"])
                country       = country_info["country"]

                #στατιστικά για τα κρούσματα
                if country_info["todayCases"] is None:
                    cases_stats = ("Δεν υπάρχουν στοιχεία κρουσμάτων.")
                elif country_info["todayCases"] > 1:
                    cases_stats = ("Καταγράφηκαν **" + f'{country_info["todayCases"]:n}' + "** κρούσματα.")
                elif country_info["todayCases"] == 1:
                    cases_stats = ("Καταγράφηκε μονάχα **ένα κρούσμα**.")
                else:
                    cases_stats = ("Κανένα κρούσμα 😄.")

                cases_stats += " (**" + f'{country_info["cases"]:n}' + "** συνολικά κρούσματα)"
                
                #στατιστικά για τους θανάτους
                if country_info["todayDeaths"] is None:
                    death_stats = ("Δεν υπάρχουν στοιχεία.")
                elif country_info["todayDeaths"] > 1:
                    death_stats = ("Σημειώθηκαν **" + f'{country_info["todayDeaths"]:n}' + "** θάνατοι.")
                elif country_info["todayDeaths"] == 1:
                    death_stats = ("Σημειώθηκε μονάχα **ένας θάνατος**.")
                else:
                    death_stats = ("Κανένας θάνατος 🥳.")

                death_stats += " (**" + f'{country_info["deaths"]:n}' + "** συνολικοί θάνατοι)"

                embedded_message = discord.Embed(title=country_emoji + " " + country, description="Στοιχεία θανάτων και κρουσμάτων COVID-19 **__για " + kataliksi + "__**.")

                embedded_message.add_field(name="Κρούσματα 🦠", value=cases_stats)
                embedded_message.add_field(name="Θάνατοι ☠"   , value=death_stats)

                embedded_message.set_footer(text="Στοιχεία από https://corona.lmao.ninja/")


                #αποστολή μηνύματος με συγχώνευση των παραπάνω
                await message.channel.send(embed=embedded_message)
            except IndexError as e:
                await message.channel.send('Δεν βρήκα αυτήν την χώρα. 😫 (Η χώρα που ψάχνεις, θα πρέπει να είναι υποχρεωτικά στα Αγγλικά. Π.χ. "GR" ή "GRC" ή "Greece")')
            except Exception as e:
                print(e.args)
                await message.channel.send('Κάτι πήγε λάθος με αυτήν τη χώρα. 🙄 (Δοκίμασε να γράψεις την χώρα με ολόκληρο το όνομά της, π.χ. "Greece")')

            return
            
    #Εδώ ελέγχουμε αν έχει σταλεί κάποιο μήνυμα σε library χωρίς φωτογραφία
    if message.channel.category_id == 749958245203836939 and not message.attachments:
        random_warning_message = random.choice(warning_messages)
        await message.delete()
        await message.channel.send(random_warning_message, delete_after=8.0)
        return

    #Το bot πλέον απαντάει όταν το κάνει mention κάποιος.
    if "<@!640605837102022696>" in message.content:
        random_complaint = random.choice(complaints)
        await message.channel.send(random_complaint)

    if "nibbaebi" in message.content.lower():
        await message.delete()
        await message.author.move_to(None)
        channel_log("Attempted to disconnect " + message.author.name + " from a voice channel (Nibbaebi.)")
        await message.channel.send("Give this mothafucka a 27 minute ban for being toxic, I'm French. (Κατουράω το Miliobot)")
        
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