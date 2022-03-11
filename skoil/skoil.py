import discord

class Skoil:
        
    def __init__(self, client):
        self.client = client

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
