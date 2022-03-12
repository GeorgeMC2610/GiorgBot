import discord
import datetime

class Common:

    #ctx is going to be the message we sent.
    def __init__(self, ctx, skoil):
        self.ctx = ctx
        self.skoil = skoil

    async def ping(self):
        await self.ctx.channel.send("Pong!")

    async def help(self):
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
        
        try:
            await self.ctx.channel.send(help_message)
        except:
            await self.ctx.author.send(help_message)

    async def corona(self, country):
        #this needs parsing.
        return
        
    async def emvolio(self, perif):
        #this also needs parsing.
        return