# GiorgBot

A simple bot written in Python 3 using the <a href="https://discordpy.readthedocs.io/en/stable/">discord.py</a> API.

## What does it do?

This is my personal bot written in Python 3. It acts like a **robot administrator** or **assistant moderator** to my personal server. A lot ot features are added just for fun or as a challenge, to test my skills in programming.

<br>

## What capabilities does it have?

This bot is capable of many things. The most important functions to add were mostly things that had to be done automatically. But, in general:

### Removing unwanted messages

Many messages are considered "unwanted", but only on several text channels. There are two cases, where they get removed immediately.

1. In the server there are several channels, called "libraries", where no text messages are allowed. As soon as a text message appears in any of those channels, the bot immediately removes it. The user that sent the messages gets informed about this (locally, not with a DM) with a "funny" message.

2. Me and the other server adminstrator thought that it would be nicer to have a separate text channel only to execute bot commands, so the general chat doesn't get messy. So, for that reason, every time a bot command is found outside the bot-requests channel, the command is immediately removed. As mentioned above, the user gets informed in the same way.

### 
