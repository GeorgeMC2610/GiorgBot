import discord

class Skoil:
        
    def __init__(self, client):
        self.client = client
        
        #bot requests denying messages.
        self.deny1 = "Ξέρεις κάτι; **Όχι**, δεν θα κάνω αυτό που θες... τι το 'χουμε το " + '<#518904659461668868>' + " ΒΡΕ ΜΑΛΑΚΑ; Αν θες πραγματικά να γίνει αυτό που θες, στείλ' το εκεί."
        self.deny2 = "Σου 'χω πει την ιστορία, όπου ένας άνθρωπος στέλνει τις εντολές του **ΟΝΤΩΣ** στο " + '<#518904659461668868>' + ";"
        self.deny3 = "Κάθε φορά που στέλενεις εντολή έξω από το" + '<#518904659461668868>' + " ένα κουταβάκι πεθαίνει... 😥"
        self.deny4 = "Γράψε 100 φορές στο τετράδιο σου 'ΘΑ ΣΤΕΛΝΩ ΤΙΣ ΕΝΤΟΛΕΣ ΜΟΥ ΜΟΝΟ ΣΤΟ " + '<#518904659461668868>' + "'." 
        self.deny5 = "Στείλ' το στο " + '<#518904659461668868>' + ", αλλιώς θα το πω στην κυρίααα 😨."
        self.deny6 = "🤡  ← εσύ, όταν δεν στέλνεις τις εντολές σου στο " + '<#518904659461668868>' + "."
        self.deny7 = "Θα έβαζες ποτέ το ψυγείο στο μπαλκόνι; Όχι. Μην βάζεις εντολές **έξω** του " + '<#518904659461668868>' + ", τότε **__ΒΛΑΚΑ__**."
        self.deny8 = "Έχω πει 500 135.000 φορές να τα στέλνεις στο " + '<#518904659461668868>' + "..."
        self.deny9 = "🚓🚓 **ΑΣΤΥΝΟΜΙΑ ΒΛΑΚΕΙΑΣ!** Ήμουν σίγουρος, ότι κάποιος σαν κι εσένα, θα έστελνε εντολή εκτός του " + '<#518904659461668868>' + "!"

        self.denying_messages = [self.deny1, self.deny2, self.deny3, self.deny4, self.deny5, self.deny6, self.deny7, self.deny8, self.deny9]

    async def initiate(self):

        #server
        self.guild = await self.client.fetch_guild(322050982747963392)

        #important members
        self.GeorgeMC2610 = await self.client.fetch_user(250721113729007617)
        self.Sotiris168   = await self.client.fetch_user(250973577761783808)

        #important roles
        self.metzi_tou_neoukti = self.guild.get_role(488730147894198273)
        self.skase             = self.guild.get_role(821739015970619393)
        self.bots              = self.guild.get_role(456219306468966410)
        self.pcmci             = self.guild.get_role(488730461091135488)
        self.me_meson          = self.guild.get_role(654344275412385793)

        #important text channels
        self.geniki_sizitisi = await self.client.fetch_channel(518905389811630087)
        self.bot_requests    = await self.client.fetch_channel(518904659461668868)

        
    def identify_member_position(self, member):

        if member.top_role == self.metzi_tou_neoukti:
            return 5

        if member.top_role == self.skase:
            return 4

        if member.top_role == self.bots:
            return 3

        if member.top_role == self.pcmci:
            return 2

        if member.top_role == self.me_meson:
            return 1
        
        return 0
