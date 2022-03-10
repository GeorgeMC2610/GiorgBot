import discord

class Skoil:
    
    command = ''
    
    client = discord.Client()
    intents = discord.Intents.default()
    intents.members = True

    guild = client.get_guild(322050982747963392)

    def identify_member_position(member):

        metzi_tou_neoukti = Skoil.guild.get_role(488730147894198273)
        if member.top_role == metzi_tou_neoukti:
            return 5

        skase = Skoil.guild.get_role(821739015970619393)
        if member.top_role == skase:
            return 4

        bots = Skoil.guild.get_role(456219306468966410)
        if member.top_role == bots:
            return 3

        pcmci = Skoil.guild.get_role(456219306468966410)
        if member.top_role == pcmci:
            return 2

        me_meson = Skoil.get_role(654344275412385793)
        if member.top_role == me_meson:
            return 1
        
        return 0
