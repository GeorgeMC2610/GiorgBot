import discord
import datetime
from dateutil import parser
from pyparsing import RecursiveGrammarException
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
        
        everything = self.recognize_area_and_date(perif, r"(ΟΛΟ)|(ΟΛΟΙ)|(ΟΛΑ)|(ΣΥΝΟΛΟ)|(ΣΥΝΟΛΙΚΑ)|(ΕΛΛΑΔΑ)|(ΧΩΡΑ)|(ΠΑΝΤΕΣ)", 0)  #get all vaccination records.
        periferia = [self.recognize_area_and_date(perif, data["area"], 0) for data in response if self.recognize_area_and_date(perif, data["area"], 0) is not None]  #get only the records that match the area the user is looking for.

        #if nothing was found, then inform the user and abort.
        if everything is None and periferia == []:
            await self.ctx.channel.send("Δεν υπάρχει αυτό που γράφεις. Δες `/help` για τον χειρισμό.")
            return
        #the second element of the tuple is the date. if the date is none, inform the user and abort.
        elif (everything is not None and everything[1] is None) or (periferia != [] and periferia.pop()[1] is None):
            await self.ctx.channel.send("Θα πρέπει να στείλεις μία σωστή ημερομηνία.")
            return
        
        #get the date
        date = everything[1] if everything is not None else periferia.pop()[1]

        #get the vaccination records
        url = 'https://data.gov.gr/api/v1/query/mdg_emvolio?date_from=' + str(date) + ' &date_to=' + str(date)
        headers = {'Authorization':'Token ' + emvolioapi}
        response = requests.get(url, headers=headers)
        response = response.json()


        await self.ctx.channel.send("Θα σου δείξω αμέσως.")


    def recognize_area_and_date(self, ipt, rgx, index):

        match = regex.search(rgx, ipt)
        if match is None:
            return None
        
        elif match.start() != index:
            return None
        
        #the area is nothing but the regex we found
        area = ipt[match.start() : match.end()]
        #the date is anything after the regex
        date = ipt[match.end() + 1 : ]

        #the default date is today.
        if len(date) == 0:
            return area, datetime.date.today()
        #the day before yesterday
        elif date == "ΠΡΟΧΘΕΣ" or date == "ΠΡΟΧΤΕΣ":
            return area, datetime.date.today() - datetime.timedelta(days=2)
        #yesterday
        elif date == "ΧΘΕΣ" or date == "ΧΤΕΣ":
            return area, datetime.date.today() - datetime.timedelta(days=1)
        #today
        elif date == "ΣΗΜΕΡΑ":
            return area, datetime.date.today()
        #else it must be a datetime.
        else:
            try:
                date = parser.parse(date)
                return area, date
            except:
                return area, None




            



    
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
