# GiorgBot

A simple bot written in Python 3 using the <a href="https://discordpy.readthedocs.io/en/stable/">discord.py</a> API.

## What does it do?

This is my personal bot written in Python 3. It acts like a **robot administrator** or **assistant moderator** to my personal server. A lot ot features are added just for fun or as a challenge, to test my skills in programming.

<br>

## What admin capabilities does it have?

This bot is capable of many things. The most important functions to add were mostly things that had to be done automatically. But, in general:

### Removing Unwanted Messages

Many messages are considered "unwanted", but only on several text channels. There are two cases, where they get removed immediately.

1. In the server there are several channels, called "libraries", where no text messages are allowed. As soon as a text message appears in any of those channels, the bot immediately removes it. The user that sent the messages gets informed about this (locally, not with a DM) with a "funny" message, which is then also removed.

2. Me and the other server adminstrator thought that it would be nicer to have a separate text channel only to execute bot commands, so the general chat doesn't get messy. So, for that reason, **every time a bot command is found outside the bot-requests channel, the command is immediately removed.** As mentioned above, the user gets informed in the same way.

### Giving Roles

I know this might sound cliche, but the bot is capable of giving reaction-based roles for one's interests. Not only does the bot immediately give or remove the roles to every user, it also checks that they're right after they're given. This happens, because the bot might be offline for a long time.

### Announcing Secret Santas

In this server, almost every Christmas (and some New Year's Days), we run an event with secret santas. The bot announces to every user, participating in the event, their own secret santa! This happens by randomly matching all the participants in the event.

### Pruning Messages

Sometimes, deleting messages en masse can be a huge pain. So, I coded my bot so that **it deletes messages in a large scale**. By using the command `giorg prune <1-50>` it can delete up to 50 consecutive messages.

### Other

Just for fun, I implemented some commands that make the bot send messages to other users or specific channels. I usually use this to mess with some of my friends, by sending them random messages using the bot.

<br>

## How can common members use this bot?

There are not many things a common user can do with this bot. But some fun usages were added during COVID-19 pandemic, using some public APIs.

### Displaying COVID-19 Data

Using the API [disease.sh](https://disease.sh/), **I was able to draw data about the COVID-19 cases and deaths for every country in the world.** So, using the command `giorg corona <country> [date]` all the users could see all the stats that the API had available.

### Displaying Vaccination Data

Greece's National Digital Governance website (gov.gr) has many sectors, one of which is **data**. The data website [data.gov.gr](data.gov.gr) has many stats available for several topics about Greece. One can request an API key to draw data about all of these topics, which is what I did. **So, using this API, I was able to draw data about vaccinations from all around Greece.** Using `giorg emvolio <region>` a member could see all vaccination data for a specific day. ("Emvolio", gr: "Εμβόλιο" stands for "vaccine")
