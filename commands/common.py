import discord
import datetime
from dateutil import parser
import flag
import requests
import locale
import re as regex

class Common:

    #ctx is going to be the message we sent.
    def __init__(self, ctx, skoil):
        self.ctx = ctx
        self.skoil = skoil

    async def safe_send(self, message, embed=None):

        if embed is None:
            try:
                await self.ctx.channel.send(message)
            except:
                await self.ctx.author.send(message)
        else:
            try:
                await self.ctx.channel.send(message, embed=embed)
            except:
                await self.ctx.author.send(message, embed=embed)

    async def ping(self):

        #this command can be executed either in a pm or server channel.
        await self.safe_send("Pong!")

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
        
        await self.safe_send(help_message)

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
            await self.safe_send('```py\n ' + str(periferies) + '```\n ● **' + str(len(periferies)) + '** συνολικές περιφερειακές ενότητες.')
            return
        
        everything = self.recognize_area_and_date(perif, r"(ΟΛΟ)|(ΟΛΟΙ)|(ΟΛΑ)|(ΣΥΝΟΛΟ)|(ΣΥΝΟΛΙΚΑ)|(ΕΛΛΑΔΑ)|(ΧΩΡΑ)|(ΠΑΝΤΕΣ)", 0)  #get all vaccination records.
        periferia = [self.recognize_area_and_date(perif, data["area"], 0) for data in response if self.recognize_area_and_date(perif, data["area"], 0) is not None]  #get only the records that match the area the user is looking for.
        periferia = periferia.pop() if periferia != [] else None

        #if nothing was found, then inform the user and abort.
        if everything is None and periferia is None:
            await self.safe_send("Δεν υπάρχει αυτό που γράφεις. Δες `/help` για τον χειρισμό.")
            return
        #the second element of the tuple is the date. if the date is none, inform the user and abort.
        elif (everything is not None and everything[1] is None) or (periferia is not None and periferia[1] is None):
            await self.safe_send("Θα πρέπει να στείλεις μία σωστή ημερομηνία.")
            return
        
        #get the date
        date = everything[1] if everything is not None else periferia[1]

        #get the vaccination records from the specific date
        url = 'https://data.gov.gr/api/v1/query/mdg_emvolio?date_from=' + str(date) + ' &date_to=' + str(date)
        headers = {'Authorization':'Token ' + emvolioapi}
        response = requests.get(url, headers=headers)
        response = response.json()

        #get the vaccinations
        total = sum([data["totalvaccinations"] for data in response]) if everything is not None else [data["totalvaccinations"] for data in response if data["area"] == periferia[0]].pop()
        dose1 = sum([data["totaldose1"] for data in response]) if everything is not None else [data["totaldose1"] for data in response if data["area"] == periferia[0]].pop()
        dose2 = sum([data["totaldose2"] for data in response]) if everything is not None else [data["totaldose2"] for data in response if data["area"] == periferia[0]].pop()
        dose3 = sum([data["totaldose3"] for data in response]) if everything is not None else [data["totaldose3"] for data in response if data["area"] == periferia[0]].pop()

        #get the daily vaccinations
        daily_total = sum([data["daytotal"] for data in response]) if everything is not None else [data["daytotal"] for data in response if data["area"] == periferia[0]].pop()
        daily_dose1 = sum([data["dailydose1"] for data in response]) if everything is not None else [data["dailydose1"] for data in response if data["area"] == periferia[0]].pop()
        daily_dose2 = sum([data["dailydose2"] for data in response]) if everything is not None else [data["dailydose2"] for data in response if data["area"] == periferia[0]].pop()
        daily_dose3 = sum([data["dailydose3"] for data in response]) if everything is not None else [data["dailydose3"] for data in response if data["area"] == periferia[0]].pop()

        #get the percentage of people done with the vaccination.
        percentage_done       = str(round(float(dose2*100/ (10720000 if everything is not None else [data["totaldistinctpersons"] for data in response if data["area"] == periferia[0]].pop()) ), 1)) + '%'
        percentage_additional = str(round(float(dose3*100/ (10720000 if everything is not None else [data["totaldistinctpersons"] for data in response if data["area"] == periferia[0]].pop()) ), 1)) + '%'

        #factor will make more and more green the embedded message's color
        factor = float(dose3/ (10720000 if everything is not None else [data["totaldistinctpersons"] for data in response if data["area"] == periferia[0]].pop()))
        r = round(255 - 364*factor) if 255 - 364*factor > 0 else 0
        g = round(255 - factor*64) if factor < 0.7 else round(180 - factor*64)
        b = round(255 - 364*factor) if 255 - 364*factor > 0 else 0

        locale.setlocale(locale.LC_ALL, 'el_GR')

        #construct the embedded message
        color = discord.embeds.Colour.from_rgb(r,g,b)
        embedded_message = discord.Embed(title=(flag.flag('gr') + " ΣΥΝΟΛΙΚΟΙ ΕΜΒΟΛΙΑΣΜΟΙ") if everything is not None else ('📍 ΠΕΡΙΦΕΡΕΙΑΚΗ ΕΝΟΤΗΤΑ ' + periferia[0]), description="Αναλυτικοί εμβολιασμοί **__για " + str(date) + "__**.", color=color)
        embedded_message.set_thumbnail(url="https://www.gov.gr/gov_gr-thumb-1200.png")
        embedded_message.add_field(name="Τουάχιστον 1️⃣ Δόση", value='Έγιναν **' + f'{daily_dose1:n}' + '** εμβολιασμοί. (**' + f'{dose1:n}' + '** σύνολο)', inline=True)
        embedded_message.add_field(name="Ολοκληρωμένοι ☑",    value='Έγιναν **' + f'{daily_dose2:n}' + '** εμβολιασμοί. (**' + f'{dose2:n}' + '** σύνολο)', inline=True)
        embedded_message.add_field(name="Ενισχυτικοί ⏫",     value='Έγιναν **' + f'{daily_dose3:n}' + '** εμβολιασμοί. (**' + f'{dose3:n}' + '** σύνολο)', inline=True)
        embedded_message.add_field(name="Αθροιστικά 💉",      value='Έγιναν **' + f'{daily_total:n}' + '** εμβολιασμοί. (**' + f'{total:n}' + '** σύνολο)', inline=True)

        if everything is not None:
            days_left = round((10720000*0.7 - daily_dose3) / (daily_dose3 if daily_dose3 != 0 else 1))
            tempo = ((str(days_left // 30) + ' μήνες' if days_left // 30 != 1 else 'έναν μήνα') if days_left // 30 > 0 else '') + (' και ' if days_left - 30*(days_left // 30) > 0 and days_left // 30 > 0 else '') + ((str(days_left - 30*(days_left // 30)) + ' ημέρες' if days_left - 30*(days_left // 30) != 1 else 'μία ημέρα') if days_left - 30*(days_left // 30) > 0 else ' λιγότερο από μία μέρα')
            embedded_message.add_field(name="Ρυθμός 🕗", value=(("Με αυτά τα δεδομένα, σε **" + tempo + "** θα έχει εμβολιαστεί το 70% του πληθυσμού.") if days_left > 1 else "Έχει εμβολιαστεί __πλήρως__ το **70% του πληθυσμού!** 🎉"), inline=True)

        embedded_message.add_field(name="Πληρότητα ✅", value="Το **" + percentage_done.replace('.', ',') + "** του πληθυσμού έχει __τελειώσει__ με τον εμβολιασμό και το **" + percentage_additional.replace('.', ',') + "** έχει λάβει την __επιπρόσθετη δόση__.", inline=True)
        embedded_message.set_footer(text="Δεδομένα από το https://emvolio.gov.gr/")

        await self.safe_send('', embed=embedded_message)


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
