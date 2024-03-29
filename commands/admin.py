import discord
import json
import random

class Admin:

    #ctx is going to be the message
    def __init__(self, ctx, skoil):
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


    async def send(self, message):

        #this command is pm only. Abort if the command is not sent in pm.
        if self.ctx.channel.type != discord.ChannelType.private:
            await self.ctx.author.send("Αυτή η εντολή εκτελείται μονάχα σε private channel. Στείλε μου την εντολή σε pm.")
            return

        #test for json syntax
        if '{' in message and message[-1] == '}' and '"target"' in message and '"message"' in message:
            payload = 0
            try:
                payload = json.loads(message)
            except:
                await self.ctx.author.send("Είσαι πολύ ηλίθιος, αν δεν ξέρεις ούτε σωστή **JSON** να γράφεις. 😣")
                return

            #initialize paylods
            targetID = False
            users = []
            async for member in self.skoil.guild.fetch_members():
                users.append(member)

            #try to retrieve id to send message.
            try:
                targetID = [i.id for i in users if str(i) == payload["target"]].pop()
                await self.ctx.author.send("🔔 Αμέσως! Στέλνω μήνυμα προς **" + payload["target"] + "**.")
            except Exception as e:
                print("Unable to decode dictionary.", e.args)
                await self.ctx.author.send('❌ **ΚΑΤΙ ΠΑΕΙ ΛΑΘΟΣ.**\n\n Σωστός χειρισμός εντολής:\n```json\n{"message":"<μήνυμα>", "target":"Χρήστης#1234"}```')
            
            #try to send the message
            if targetID:

                try:
                    user_to_send = self.skoil.client.get_user(targetID)
                    await user_to_send.send(payload["message"])
                    await self.ctx.author.send("Έφτασε το μήνυμα! ✅")
                except Exception as e:
                    print("Unable to send to user. User may have disabled bot sends", e.args)
                    await self.ctx.author.send(f'❌ **ΚΑΤΙ ΠΑΕΙ ΛΑΘΟΣ.** Πιθανότατα το άτομο {str(user_to_send)} να έχει __απενεργοποιήσει__ μηνύματα από bots.')


    async def announce_bot(self, message):

        #this command is pm only. Abort if the command is not sent in pm.
        if self.ctx.channel.type != discord.ChannelType.private:
            await self.ctx.author.send("Αυτή η εντολή εκτελείται μονάχα σε private channel. Στείλε μου την εντολή σε pm.")
            return

        #send the message in the geniki-sizitisi channel
        await self.skoil.bot_requests.send(message)


    async def announce_geniki(self, message):
        
        #this command is pm only. Abort if the command is not sent in pm.
        if self.ctx.channel.type != discord.ChannelType.private:
            await self.ctx.author.send("Αυτή η εντολή εκτελείται μονάχα σε private channel. Στείλε μου την εντολή σε pm.")
            return

        #send the message in the geniki-sizitisi channel
        await self.skoil.geniki_sizitisi.send(message)


    async def announce(self, message):

        #this command is pm only. Abort if the command is not sent in pm.
        if self.ctx.channel.type != discord.ChannelType.private:
            await self.ctx.author.send("Αυτή η εντολή εκτελείται μονάχα σε private channel. Στείλε μου την εντολή σε pm.")
            return

        #check if the message has the right json syntax
        if '{' in message and message[-1] == '}' and '"channel"' in message and '"message"' in message:
            payload = 0
            try:
                payload  = json.loads(message)
            except:
                await self.ctx.author.send("Είσαι πολύ ηλίθιος, αν δεν ξέρεις ούτε σωστή **JSON** να γράφεις 🙄")
                return

            #the target ID will be the corresponding channel.
            targetID = False
            channels = await self.skoil.guild.fetch_channels()

            try:
                #from all the channels select the right one.
                targetID = [i.id for i in channels if i.name == payload["channel"]].pop()
                await self.ctx.author.send("🔔 Εννοείται πως θα το ανακοινώσω στο <#" + str(targetID) + ">")
            except Exception as e:
                #if the channel doesn't exist.
                print("Unable to decode dictionary.", e.args)
                await self.ctx.author.send("❌ Δεν το βρήκα αυτό ρε φίλε :(")
            
            if targetID:
                channel = self.skoil.client.get_channel(targetID)
                await channel.send(payload["message"])
                await self.ctx.author.send("Έφτασε! ✅")
            else:
                await self.ctx.author.send('❌ **ΝΑΙ, ΑΛΛΑ ΟΧΙ.**\n\n Σωστός χειρισμός εντολής:\n```json\n{"message":"<μήνυμα>", "channel":"akrives-onoma-kanaliou"}```')


    async def prune(self, times):

        if self.ctx.channel.type == discord.ChannelType.private:
            await self.ctx.author.send("Αυτή η εντολή εκτελείται μονάχα σε text-channel στον ΣΚΟΪΛ ΕΛΙΚΙΚΟΥ. Στείλε μου την εντολή σε ένα από αυτά τα channels.")
            return

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

        #this command has no restrictions regarding private messages or text-channels. It can be executed in either one of those types.

        members = await self.skoil.guild.fetch_members().flatten()
        await self.safe_send("```python\n" + str([member.name for member in members]) + "```\n\n**" + str(len(members)) + " συνολικά μέλη,** όπου τα " + str(len([member for member in members if self.skoil.identify_member_position(member) == 3])) + " είναι bots.")


    async def secret_santa(self):
        
        #method to ensure that no one is the secret santa of themselves.
        def no_duplicates(list1, list2):
            random.shuffle(list2)
            for member1, member2 in zip(list1, list2):
                if member1 == member2 or (member1.name == "xanthosgeorge" and member2.name == "GeorgeMC2610") or (member1.name == "Sotiris168" and member2.name == "Lefteris36") or (member1.name == "Aemilius" and member2.name == "Sotiris168"):
                    no_duplicates(list1, list2)
            
            return list2

        #fetch users that are present in the event.
        event = await self.skoil.guild.fetch_scheduled_event(1057065317379084368)
        members = []
        async for user in event.users():
            members.append(user)

        #ensure that no secret santa is a duplicate.
        santas = members.copy()
        santas = no_duplicates(members, santas)

        #announce secret santa events
        for member1, member2 in zip(members, santas):
            try:
                await member1.send(f'Ήρθε η μεγάλη στιγμή, κύριε {member1.name}. **Είσαι ο secret santa του {str(member2)}.** Καλή τύχη!')
            except:
                await self.skoil.GeorgeMC2610.send(f'Δεν μπορώ να στείλω μήνυμα στον {str(member1)} για τον {member2}')


    async def add_library(self, id):

        #this command is executed inside a server text-channel.
        if self.ctx.channel.type == discord.ChannelType.private:
            await self.ctx.author.send("Αυτή η εντολή εκτελείται μονάχα σε text-channel σε κάποιον server.")
            return

        try:

            #turn the id into an integer.
            id = int(id)

            

        except Exception as e:

            #
            await self.ctx.channel.send("ΣΤΕΙΛΕ ΑΡΙΘΜΟ, ΗΛΙΘΙΕ.")
            print(e.args)
            return