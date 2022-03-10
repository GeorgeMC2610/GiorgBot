import discord
import datetime

class Common:

    command_dict = {
        'ping'            : None,
        'help'            : None,
        'announce'        : [str],
        'prune'           : [int],
        'corona'          : [str, datetime],
        'emvolio'         : [str, datetime]
    }

    async def ping(ctx):
        await ctx.channel.send("Pong!")
    