import discord
from skoil.skoil import Skoil

class Admin:

    #ctx is going to be the message
    def __init__(self, ctx, skoil):

        #check to see if the admin command to be executed is in private messages. If it is, only GeorgeMC2610 and Sotiris168 should be able to execute it.
        if ctx.channel.type == discord.ChannelType.private:
            if not(ctx.author == skoil.GeorgeMC2610 or ctx.author == skoil.Sotiris168):
                self.ctx = None
                return None
        #check to see if the admin command to be executed is sent by a member with admin/mod previleges.
        elif skoil.identify_member_position(ctx.author) < 4:
            self.ctx = None
            return None

        #otherwise, at this point, it's safe to execute the admin command.
        self.ctx = ctx
        

    async def announce_bot(self, message):
        pass


    async def announce_geniki(self, message):
        pass


    async def announce(self, message):
        pass


    async def prune(self, times):

        

        if len(times) > 1:
            await self.ctx.channel.send("Όχι. Μάθε να γράφεις σωστά το command")
            return

        times = times.pop()

        #the number of times must be an integer.
        try:
            times = int(times)
            #if the number of times is a specific meme number, send a message
            if times == 42069 or times == 69420 or times == 69 or times == 420:
                await self.ctx.channel.send("Ναι, ναι ΧΑ-ΧΑ. Πολύ αστείο, γαμημένε.")
                return
            #maximum number of messages to be deleted is 50.
            elif times > 50:
                await self.ctx.channel.send("ΤΙ ΛΕΤΕ ΚΥΡΙΕ; ΜΑΞ 50 ΜΗΝΥΜΑΤΑ. ΚΑΙ ΠΟΛΛΑ ΕΙΝΑΙ ΜΗ ΣΟΥ ΠΩ.")
                return
            #messages have to be a positive number.
            elif times < 0:
                await self.ctx.channel.send("Και για πες, βρε μαλάκα... Πώς θα σβήσω αρνητικό αριθμό μηνυμάτων;")
                return

            await self.ctx.delete()
            async for message_to_be_deleted in self.ctx.channel.history(limit=times):
                await message_to_be_deleted.delete()
        except Exception as e:
            await self.ctx.channel.send("ΣΤΕΙΛΕ ΑΡΙΘΜΟ, ΗΛΙΘΙΕ.")
            print(e.args)
            return
        


    async def display_members(self):
        pass


    async def secret_santa(self):
        pass