import discord

class Skoil:
        
    def __init__(self, sender, client):
        self.client = client
        self.sender = sender

    async def initiate(self):
        self.guild = await self.client.fetch_guild(322050982747963392)

        if self.sender == 'admin':
            self.GeorgeMC2610 = await self.client.fetch_user(250721113729007617)
            self.Sotiris168   = await self.client.fetch_user(250973577761783808)
            self.metzi_tou_neoukti = self.guild.get_role(488730147894198273)
        
    def identify_member_position(self, member):

        self.metzi_tou_neoukti = self.guild.get_role(488730147894198273)
        if member.top_role == self.metzi_tou_neoukti:
            return 5

        self.skase = self.guild.get_role(821739015970619393)
        if member.top_role == self.skase:
            return 4

        self.bots = self.guild.get_role(456219306468966410)
        if member.top_role == self.bots:
            return 3

        self.pcmci = self.guild.get_role(456219306468966410)
        if member.top_role == self.pcmci:
            return 2

        self.me_meson = self.get_role(654344275412385793)
        if member.top_role == self.me_meson:
            return 1
        
        return 0
