import discord

class Admin:

    #ctx is going to be the message
    def __init__(self, ctx):
        self.ctx = ctx

    async def prune(ctx):
        return