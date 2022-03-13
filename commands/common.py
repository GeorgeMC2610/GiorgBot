import discord
import datetime
import requests
import re as regex

class Common:

    #ctx is going to be the message we sent.
    def __init__(self, ctx, skoil):
        self.ctx = ctx
        self.skoil = skoil

    async def ping(self):

        #this command can be executed either in a pm or server channel.

        try:
            await self.ctx.channel.send("Pong!")
        except:
            await self.ctx.author.send("Pong!")

    async def help(self):

        #this command can be executed either in a pm or server channel.

        help_dialog1 = '**ΔΙΚΕΣ ΜΟΥ ΕΝΤΟΛΕΣ:**'
        help_dialog2 = '`giorg help` → Δείχνει το παρόν μενού.'
        help_dialog3 = '`giorg ping` → Ανταπόκριση του μποτ με "Pong!"'
        help_dialog4 = '`giorg emvolio <όνομα περιφερειακής ενότητας>` → Προβολή των συνολικών και ημερίσιων εμβολιασμών της περιφερειακής ενότητας.'
        help_dialog5 = '`giorg emvolio <σύνολο|όλα|όλο|Ελλάδα|χώρα|συνολικά|πάντες>` → Προβολή των συνολικών και ημερίσιων εμβολιασμών όλης της Ελλάδας.'
        help_dialog6 = '`giorg emvolio <περιφέρειες|περιφερειακές ενότητες|λίστα|ενότητες|περιοχές>` → Προβολή των διαθέσιμων περιοχών, για την ανάκτηση δεδομένων του εμβολίου.'
        help_dialog7 = '`giorg corona <χώρα στα αγγλικά>` → Προβολή συνολικών και ημερισίων κρουσμάτων και θανάτων από την COVID-19 της επιλεγμένης χώρας.'
        help_dialog8 = '`giorg corona <list|all|countries>` → Προβολή των διαθέσιμων χωρών, για ανάκτηση στατιστικών στοιχείων περί COVID-19 (κρούσματα & θάνατοι).'
        help_dialog9 = '**ΕΝΤΟΛΕΣ ΔΙΑΧΕΙΡΙΣΤΗ:**'
        help_dialog94 = '`giorg display members` → Προβολή όλων των μελών του σέρβερ.' 
        help_dialog95 = '`giorg prune <αριθμός 1-50>` → Σβήσιμο όλων των προηγούμενων μηνυμάτων"'
        help_dialog96 = '`giorg announcegeniki <μήνυμα>` → Άμεση αποστολή μηνύματος, από εμένα, στο κανάλι <#518905389811630087>'
        help_dialog97 = '`giorg announcebot <μήνυμα>` → Άμεση αποστολή μηνύματος, από εμένα, στο κανάλι <#518904659461668868>'
        help_dialog98 = '`giorg announce {"channel":"<ακριβές όνομα καναλιού>", "message":"<μήνυμα>"}` → Άμεση αποστολή μηνύματος, από εμένα, σε συγκεκριμένο κανάλι που ορίζεται στο πεδίο `channel`.'
        help_dialog99 = '`giorg send {"target":"Χρήστης#1234", "message":"<μήνυμα>"}` → Άμεση αποστολή μηνύματος, από εμένα, σε οποιοδήποτε μέλος του server.'

        help_message = help_dialog1 + '\n' + help_dialog2 + '\n' + help_dialog3 + '\n' + help_dialog4 + '\n' + help_dialog5 + '\n' + help_dialog6 + '\n' +  help_dialog7 + '\n' + help_dialog8 + '\n\n' + help_dialog9 + '\n' + help_dialog94 + '\n' + help_dialog95  + '\n' + help_dialog96 + '\n' + help_dialog97  + '\n' + help_dialog98 + '\n' + help_dialog99
        
        try:
            await self.ctx.channel.send(help_message)
        except:
            await self.ctx.author.send(help_message)

    async def corona(self, country):
        #this needs parsing.
        return
        
    async def emvolio(self, perif):

        #get the api token
        f = open('emvolioapi.txt', 'r')
        emvolioapi = f.read()
        f.close()

        perif = perif.upper()
        perif = self.remove_greek_uppercase_accent(perif)

        #get all the available cities.
        url = 'https://data.gov.gr/api/v1/query/mdg_emvolio?date_from=2020-12-30&date_to=2020-12-30'
        headers = {'Authorization':'Token ' + emvolioapi}
        response = requests.get(url, headers=headers)
        response = response.json()

        #if the user wants to see just the cities available, show all cities and refer to the number of cities.
        periferies = [data["area"] for data in response]
        if perif in ["ΠΕΡΙΦΕΡΕΙΕΣ", "ΠΕΡΙΦΕΡΕΙΑΚΕΣ ΕΝΟΤΗΤΕΣ", "ΛΙΣΤΑ", "ΕΝΟΤΗΤΕΣ", "ΠΕΡΙΟΧΕΣ"]:
            await self.ctx.channel.send('```py\n ' + str(periferies) + '```\n ● **' + str(len(periferies)) + '** συνολικές περιφερειακές ενότητες.')
            return
        
        #search with regex if the user wants the total vaccination records.
        everything = regex.search(r"(ΟΛΟ)|(ΟΛΟΙ)|(ΟΛΑ)|(ΣΥΝΟΛΟ)|(ΣΥΝΟΛΙΚΑ)|(ΕΛΛΑΔΑ)|(ΧΩΡΑ)|(ΠΑΝΤΕΣ)", perif)
        periferia = None
        
        #search with regex if the user wants vaccination records of one area only.
        for data in response:
            if not regex.match(data["area"], perif):
                continue

            #the area must be first.
            if regex.match(data["area"], perif).start() != 0:
                continue

            periferia = data["area"]


        if (everything is None or everything.start() != 0) and periferia is None:
            await self.ctx.channel.send("Λάθος μήνυμα. Για να δείτε όλους τους συνολικούς εμβολιασμούς, πατήστε `giorg emvolio όλο|όλοι|όλα|σύνολο|συνολικά|ελλάδα|χώρα|πάντες [ημερομηνία]`\nΑλλιώς, για να δείτε όλες τις περιφερειακές ενότητες, πατήστε `giorg emvolio λίστα`")
            return

        await self.ctx.channel.send("Θα σου δείξω αμέσως.")


            



    
    #this function removes correctly any greek uppercase accent.
    def remove_greek_uppercase_accent(self, x):
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
