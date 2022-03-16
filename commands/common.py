import discord
import datetime
from dateutil import parser
import flag
from numpy import who
import requests
import locale
import re as regex

class Common:

    #ctx is going to be the message we sent.
    def __init__(self, ctx : discord.Message, skoil):
        self.ctx = ctx
        self.skoil = skoil

    async def safe_send(self, message, embed=None):

        #safe send will send a message both to a pm and server channel
        if embed is None:
            try:
                await self.ctx.channel.send(message)
            except:
                await self.ctx.author.send(message)
        #also supports embeds
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

        help_dialog1 = '**ΔΙΚΕΣ ΜΟΥ ΕΝΤΟΛΕΣ:**\n'
        help_dialog2 = '`giorg help` → Δείχνει το παρόν μενού.\n'
        help_dialog3 = '`giorg ping` → Ανταπόκριση του μποτ με "Pong!"\n'
        help_dialog4 = '`giorg emvolio <όνομα περιφερειακής ενότητας> [κάποια ημερομηνία|σήμερα|χθες|προχθές]` → Προβολή των συνολικών και ημερίσιων εμβολιασμών της περιφερειακής ενότητας.\n'
        help_dialog5 = '`giorg emvolio <σύνολο|όλα|όλο|Ελλάδα|χώρα|συνολικά|πάντες> [κάποια ημερομηνία|σήμερα|χθες|προχθές]` → Προβολή των συνολικών και ημερίσιων εμβολιασμών όλης της Ελλάδας.\n'
        help_dialog6 = '`giorg emvolio <περιφέρειες|περιφερειακές ενότητες|λίστα|ενότητες|περιοχές>` → Προβολή των διαθέσιμων περιοχών, για την ανάκτηση δεδομένων του εμβολίου.\n'
        help_dialog7 = '`giorg corona <χώρα στα αγγλικά> [σήμερα|χθες|προχθές]` → Προβολή συνολικών και ημερισίων κρουσμάτων και θανάτων από την COVID-19 της επιλεγμένης χώρας.\n'
        help_dialog8 = '`giorg corona <list|all|countries>` → Προβολή των διαθέσιμων χωρών, για ανάκτηση στατιστικών στοιχείων περί COVID-19 (κρούσματα & θάνατοι).\n\n'
        help_dialog9 = '**ΕΝΤΟΛΕΣ ΔΙΑΧΕΙΡΙΣΤΗ:**\n'
        help_dialog94 = '`giorg display_members` → Προβολή όλων των μελών του σέρβερ.\n' 
        help_dialog95 = '`giorg prune <αριθμός 1-50>` → Σβήσιμο όλων των προηγούμενων μηνυμάτων"\n'
        help_dialog96 = '`giorg announce_geniki <μήνυμα>` → Άμεση αποστολή μηνύματος, από εμένα, στο κανάλι <#518905389811630087>\n'
        help_dialog97 = '`giorg announce_bot <μήνυμα>` → Άμεση αποστολή μηνύματος, από εμένα, στο κανάλι <#518904659461668868>\n'
        help_dialog98 = '`giorg announce {"channel":"<ακριβές όνομα καναλιού>", "message":"<μήνυμα>"}` → Άμεση αποστολή μηνύματος, από εμένα, σε συγκεκριμένο κανάλι που ορίζεται στο πεδίο `channel`.\n'
        help_dialog99 = '`giorg send {"target":"Χρήστης#1234", "message":"<μήνυμα>"}` → Άμεση αποστολή μηνύματος, από εμένα, σε οποιοδήποτε μέλος του server.\n'

        help_message = help_dialog1 + help_dialog2 + help_dialog3 + help_dialog4 + help_dialog5 + help_dialog6 + help_dialog7 + help_dialog8 + help_dialog9 + help_dialog94 + help_dialog95 + help_dialog96 + help_dialog97 + help_dialog98 + help_dialog99
        
        await self.safe_send(help_message)


    async def corona(self, country : str):
        
        #this command can be executed either in a pm or a server channel
        country = country.lower()

        #get all the available countries
        url = 'https://disease.sh/v3/covid-19/countries?yesterday=false&twoDaysAgo=false&sort=cases&allowNull=false'
        response = requests.get(url)
        response = response.json()
        countries = [data["country"] for data in response]
        iso2      = [data["countryInfo"]["iso2"] for data in response]
        iso3      = [data["countryInfo"]["iso3"] for data in response]

        #if the user wants to see all available countries
        if country in ["all", "countries", "list"]:
            countries.sort()    #sort all countries
            #break the message in two, as it is too large to be sent in one.
            await self.ctx.channel.send('```python\n' + str(countries[:len(countries)//2]) + '```')
            await self.ctx.channel.send('```python\n' + str(countries[len(countries)//2:]) + '```\n ● **' + str(len(countries)) + '** συνολικές διαθέσιμες χώρες-κλειδιά.')
            return

        #get all possible country formats
        whole_country = [self.recognize_country_and_date(country, data["country"], 0) for data in response if self.recognize_country_and_date(country, data["country"], 0) is not None]
        iso3 = [self.recognize_country_and_date(country, data["countryInfo"]["iso3"], 0) for data in response if self.recognize_country_and_date(country, data["countryInfo"]["iso3"], 0) is not None]
        iso2 = [self.recognize_country_and_date(country, data["countryInfo"]["iso2"], 0) for data in response if self.recognize_country_and_date(country, data["countryInfo"]["iso2"], 0) is not None]

        #if all are none, then there must be a mistake.
        if whole_country == [] and iso3 == [] and iso2 == []:
            await self.safe_send("Αυτή η χώρα δεν υπάρχει. Δες όλες τις διαθέσιμες χώρες πατώντας `giorg corona list`.")
            return
        
        #if we've gotten to this point, at least ONE of them has to have the data.
        data = whole_country.pop() if whole_country != [] else iso3.pop() if iso3 != [] else iso2.pop()
        country = data[0]
        yesterday = data[1]
        twoDaysAgo = data[2]

        #this is how we refer to the day.
        if yesterday:
            kataliksi = 'χθες'
        elif twoDaysAgo:
            kataliksi = 'προχθές'
        else:
            kataliksi = 'σήμερα'

        #get the current stats
        url = 'https://disease.sh/v3/covid-19/countries/' + country + '?yesterday=' + str((yesterday)).lower() + '&twoDaysAgo=' + str(twoDaysAgo).lower() + '&sort=cases&allowNull=false'
        response = requests.get(url)
        response = response.json()

        #set locale to greek, since the message is going to be in Greek.
        locale.setlocale(locale.LC_ALL, 'el_GR')

        #in order to get test data, we have to get the data for the day before the selected.
        if twoDaysAgo:
            testdiff = 0
        else:
            #with these logic values on yesterday and twodaysago, we can always get the day before.
            url = 'https://disease.sh/v3/covid-19/countries/' + country + '?yesterday=' + str((not yesterday)).lower() + '&twoDaysAgo=' + str(yesterday).lower() + '&sort=cases&allowNull=false'
            day_before = requests.get(url)
            day_before = day_before.json()

            testdiff = (response["tests"] - day_before["tests"]) if response["tests"] is not None and day_before["tests"] is not None else 0

        tests = "Το **" + str(round(response["todayCases"]*100/testdiff, 5)).replace('.', ',') + "%** των τεστ βγήκαν θετικά. (**" + f'{testdiff:n}' + "** δοκιμές)" if testdiff != 0 else "Δεν υπάρχουν στοιχεία."

        #total and today's covid cases.
        if response["todayCases"] is None or (response["todayCases"] == 0 and testdiff == 0):
            cases = "Δεν υπάρχουν στοιχεία."
        elif response["todayCases"] > 1:
            cases = "**" + f'{response["todayCases"]:n}' + "** νοσούντες."
        elif response["todayCases"] == 1:
            cases = "Μονάχα **ένα κρούσμα**."
        else:
            cases = "**Κανένα** κρούσμα! 🤩"

        cases += " (**" + f'{response["cases"]:n}' + "** συνολικά)" if response["cases"] > 1 else " (**Ένα** κρούσμα συνολικά!)" if response["cases"] == 1 else " (**Κανένα** κρούσμα συνολικά‼) 🤯"

        #total and today's covid deaths.
        if response["todayDeaths"] is None or (response["todayDeaths"] == 0 and testdiff == 0):
            deaths = "Δεν υπάρχουν στοιχεία."
        elif response["todayDeaths"] > 1:
            deaths = "**" + f'{response["todayDeaths"]:n}' + "** απώλειες."
        elif response["todayDeaths"] == 1:
            deaths = "Μονάχα **ένας θάνατος**."
        else:
            deaths = "**Κανένας** θάνατος! 🥳"

        deaths += " (**" + f'{response["deaths"]:n}' + "** συνολικά)" if response["deaths"] > 1 else " (**Ένας** θάνατος συνολικά!)" if response["deaths"] == 1 else " (**Κανένας** θάνατος συνολικά‼) 🎊"

        #total critical condition cases.
        if response["critical"] is None or (response["critical"] == 0 and testdiff == 0):
            active = "Δεν υπάρχουν στοιχεία."
        elif response["critical"] > 1:
            active = "**" + f'{response["critical"]:n}' + "** βρίσκονται σε Μ.Ε.Θ."
        elif response["critical"] == 1:
            active = "**Ένας** νοσηλεύεται σε Μ.Ε.Θ."
        else:
            active = "**Κανένας** σε κρίσιμη κατάσταση! 😁"

        #colouring factor for embedded message
        factor = float(response["active"]/response["casesPerOneMillion"]) if response["casesPerOneMillion"] != 0 else 0
        r = round(254 - factor*2) if factor*2 < 130 else 125
        g = round(255 - 254*factor) if factor < 1 else 0
        b = round(255 - 254*factor) if factor < 1 else 0

        print(r, g, b, factor)
        color = discord.embeds.Colour.from_rgb(r, g, b)

        #construct embedded message.
        embedded_message = discord.Embed(title=response["country"], description="Στοιχεία θανάτων και κρουσμάτων COVID-19 **__για " + kataliksi + "__**.", color=color)
        embedded_message.set_thumbnail(url=response["countryInfo"]["flag"])
        embedded_message.add_field(name="Κρούσματα 🦠",      value=cases,  inline=False)
        embedded_message.add_field(name="Θάνατοι ☠"   ,      value=deaths,  inline=False)
        embedded_message.add_field(name="Διασωληνωμένοι 🏥", value=active, inline=False)
        embedded_message.add_field(name="Τεστ 🧪",           value=tests,  inline=False)
        embedded_message.set_footer(text="Στοιχεία από disease.sh")

        #since this can be sent both in pm's and server channels, safely send it.
        await self.safe_send('', embed=embedded_message)   
        

    def recognize_country_and_date(self, ipt, rgx, index):
        
        #sometimes iso2 and iso3 can be none, so return none if so.
        if rgx is None:
            return None

        #rgx is the country or iso3 or iso2 we're looking for 
        match = regex.search(rgx, ipt, regex.IGNORECASE)
        if match is None:
            return None
        
        #it must also be at the selected index
        elif match.start() != index:
            return None
        
        #the country is nothing but the regex we found
        area = ipt[match.start() : match.end()]
        #the date is anything after the regex
        date = ipt[match.end() + 1 : ]
        date = self.remove_greek_uppercase_accent(date.upper())

        #RETURN PATTERN: area, yesterday, twoDaysAgo
        #the default date depends on today's hour.
        if len(date) == 0:     
            return (area, True, False) if datetime.datetime.today().hour < 18 else (area, False, False)
        #the day before yesterday
        elif date == "ΠΡΟΧΘΕΣ" or date == "ΠΡΟΧΤΕΣ":
            return area, False, True
        #yesterday
        elif date == "ΧΘΕΣ" or date == "ΧΤΕΣ":
            return area, True, False
        #today
        elif date == "ΣΗΜΕΡΑ":
            return area, False, False
        #else it's something that can't be interpreted.
        else:
            return area, None


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
        
        #get the date and the area depending on which of these values are none.
        area = everything[0] if everything is not None else periferia[0]
        date = everything[1] if everything is not None else periferia[1]

        print(str(date))

        #get the vaccination records from the specific date
        url = 'https://data.gov.gr/api/v1/query/mdg_emvolio?date_from=' + str(date) + ' &date_to=' + str(date)
        headers = {'Authorization':'Token ' + emvolioapi}
        response = requests.get(url, headers=headers)
        response = response.json()

        #get the vaccinations
        total = sum([data["totalvaccinations"] for data in response]) if everything is not None else [data["totalvaccinations"] for data in response if data["area"] == area].pop()
        dose1 = sum([data["totaldose1"] for data in response]) if everything is not None else [data["totaldose1"] for data in response if data["area"] == area].pop()
        dose2 = sum([data["totaldose2"] for data in response]) if everything is not None else [data["totaldose2"] for data in response if data["area"] == area].pop()
        dose3 = sum([data["totaldose3"] for data in response]) if everything is not None else [data["totaldose3"] for data in response if data["area"] == area].pop()

        #get the daily vaccinations
        daily_total = sum([data["daytotal"] for data in response]) if everything is not None else [data["daytotal"] for data in response if data["area"] == area].pop()
        daily_dose1 = sum([data["dailydose1"] for data in response]) if everything is not None else [data["dailydose1"] for data in response if data["area"] == area].pop()
        daily_dose2 = sum([data["dailydose2"] for data in response]) if everything is not None else [data["dailydose2"] for data in response if data["area"] == area].pop()
        daily_dose3 = sum([data["dailydose3"] for data in response]) if everything is not None else [data["dailydose3"] for data in response if data["area"] == area].pop()

        if total == 0 and daily_total == 0:
            await self.safe_send("Δεν υπάρχουν στοιχεία εμβολιασμών για αυτήν την ημέρα. **(" + str(date) + ")**")
            return

        #get the percentage of people done with the vaccination.
        percentage_done       = str(round(float(dose2*100/ (10720000 if everything is not None else [data["totaldistinctpersons"] for data in response if data["area"] == area].pop()) ), 1)) + '%'
        percentage_additional = str(round(float(dose3*100/ (10720000 if everything is not None else [data["totaldistinctpersons"] for data in response if data["area"] == area].pop()) ), 1)) + '%'

        #factor will make more and more green the embedded message's color
        factor = float(dose3/ (10720000 if everything is not None else [data["totaldistinctpersons"] for data in response if data["area"] == area].pop()))
        r = round(255 - 364*factor) if 255 - 364*factor > 0 else 0
        g = round(255 - factor*64) if factor < 0.7 else round(180 - factor*64)
        b = round(255 - 364*factor) if 255 - 364*factor > 0 else 0

        locale.setlocale(locale.LC_ALL, 'el_GR')

        #construct the embedded message
        color = discord.embeds.Colour.from_rgb(r,g,b)
        embedded_message = discord.Embed(title=(flag.flag('gr') + " ΣΥΝΟΛΙΚΟΙ ΕΜΒΟΛΙΑΣΜΟΙ") if everything is not None else ('📍 ΠΕΡΙΦΕΡΕΙΑΚΗ ΕΝΟΤΗΤΑ ' + area), description="Αναλυτικοί εμβολιασμοί **__για " + str(date) + "__**.", color=color)
        embedded_message.set_thumbnail(url="https://www.gov.gr/gov_gr-thumb-1200.png")
        embedded_message.add_field(name="Τουάχιστον 1️⃣ Δόση", value=('Έγιναν **' + f'{daily_dose1:n}' + '** εμβολιασμοί. ' if daily_dose1 > 1 else 'Μόνον **ένας** εμβολιασμός. ' if daily_dose1 == 1 else '**Κανένας** εμβολιασμός. ') + '(**' + f'{dose1:n}' + '** σύνολο)', inline=True)
        embedded_message.add_field(name="Ολοκληρωμένοι ☑",    value=('Έγιναν **' + f'{daily_dose2:n}' + '** εμβολιασμοί. ' if daily_dose2 > 1 else 'Μόνον **ένας** εμβολιασμός. ' if daily_dose2 == 1 else '**Κανένας** εμβολιασμός. ') + '(**' + f'{dose2:n}' + '** σύνολο)', inline=True)
        embedded_message.add_field(name="Ενισχυτικοί ⏫",     value=('Έγιναν **' + f'{daily_dose3:n}' + '** εμβολιασμοί. ' if daily_dose3 > 1 else 'Μόνον **ένας** εμβολιασμός. ' if daily_dose3 == 1 else '**Κανένας** εμβολιασμός. ') + '(**' + f'{dose3:n}' + '** σύνολο)', inline=True)
        embedded_message.add_field(name="Αθροιστικά 💉",      value=('Έγιναν **' + f'{daily_total:n}' + '** εμβολιασμοί. ' if daily_total > 1 else 'Μόνον **ένας** εμβολιασμός. ' if daily_total == 1 else '**Κανένας** εμβολιασμός. ') + '(**' + f'{total:n}' + '** σύνολο)', inline=True)

        if everything is not None:
            #if i were you, i wouldn't try to understand this by myself.
            #this field checks if the tempo can be added as a field. it can only be added if the user has selected to see all vaccinations.

            days_left = round((10720000*0.7 - daily_dose3) / daily_dose3 if daily_dose3 != 0 else 1) if daily_dose3 != 0 else None  #days left are calculated through a divsion operation. if the denominator is zero, the whole variable turns to none.
            tempo = ((str(days_left // 30) + ' μήνες' if days_left // 30 != 1 else 'έναν μήνα') if days_left // 30 > 0 else '') + (' και ' if days_left - 30*(days_left // 30) > 0 and days_left // 30 > 0 else '') + ((str(days_left - 30*(days_left // 30)) + ' ημέρες' if days_left - 30*(days_left // 30) != 1 else 'μία ημέρα') if days_left - 30*(days_left // 30) > 0 else ' λιγότερο από μία μέρα') if days_left is not None else 'όχι'
            embedded_message.add_field(name="Ρυθμός 🕗", value=("Δεν μπορεί να υπολογισθεί ο ρυθμός, με βάση τα παρόντα δεδομένα." if days_left is None else "Έχει εμβολιαστεί __πλήρως__ το **70% του πληθυσμού!** 🎉" if days_left < 1 else ("Με αυτά τα δεδομένα, σε **" + tempo + "** θα έχει εμβολιαστεί το 70% του πληθυσμού.")), inline=True)

        embedded_message.add_field(name="Πληρότητα ✅", value="Το **" + percentage_done.replace('.', ',') + "** του πληθυσμού έχει __τελειώσει__ με τον εμβολιασμό και το **" + percentage_additional.replace('.', ',') + "** έχει λάβει την __επιπρόσθετη δόση__.", inline=True)
        embedded_message.set_footer(text="Δεδομένα από το https://emvolio.gov.gr/")

        #send the embedded message safely, as this can be called through dm's or server channels.
        await self.safe_send('', embed=embedded_message)


    def recognize_area_and_date(self, ipt, rgx, index):

        #first we must match the input with the regex given.
        match = regex.search(rgx, ipt)
        if match is None:
            return None
        
        #it must also be at the selected index
        elif match.start() != index:
            return None
        
        #the area is nothing but the regex we found
        area = ipt[match.start() : match.end()]
        #the date is anything after the regex
        date = ipt[match.end() + 1 : ]

        #the default date depends on today's hour.
        if len(date) == 0:     
            return (area, datetime.date.today() - datetime.timedelta(days=1)) if datetime.datetime.today().hour < 21 else (area, datetime.date.today())
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
