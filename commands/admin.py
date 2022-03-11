import discord

class Admin:

    #ctx is going to be the message
    def __init__(self, ctx):
        self.ctx = ctx

    async def announce_bot(self, message):
        pass


    async def announce_geniki(self, message):
        pass


    async def announce(self, message):
        pass


    async def prune(self, times):

        #the number of times must be an integer.
        try:
            times = int(times)
        except:
            await self.ctx.channel.send("ΣΤΕΙΛΕ ΑΡΙΘΜΟ, ΗΛΙΘΙΕ.")
            return
        
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


    async def display_members(self):
        pass


    async def secret_santa(self):
        pass