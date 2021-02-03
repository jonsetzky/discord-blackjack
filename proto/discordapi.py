
import time
import discord
import asyncio
import pickle

class DiscordLogger:
    logs = dict()

    @staticmethod
    def AddSentMessage(messageObject):
        if not messageObject.channel in list(DiscordLogger.logs.keys()):
            DiscordLogger.logs[messageObject.channel] = list()
        DiscordLogger.logs[messageObject.channel].append({'msg': messageObject, 'time': time.time() })
        asyncio.get_event_loop().create_task(DiscordLogger.WriteLogs())
        DiscordLogger.WriteLogs()

    @staticmethod
    def TryDeleteSentMessage(messageObject):
        try:
            for msg in DiscordLogger.logs[messageObject.channel]:
                if messageObject.id == msg['msg'].id:
                    del msg
        except:
            return

    @staticmethod
    def WriteLogs():
        with open('log', 'wb') as f:
            pickle.dump(DiscordLogger.logs, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def ReadLogs():
        with open('log', 'rb') as f:
            DiscordLogger.logs = pickle.load(f)


class DiscordAPI:



    @staticmethod
    async def SendMessage(channel, content=None, embed=None):
        messageObject = await discord.TextChannel.send(channel, content=content, embed=embed)
        asyncio.get_event_loop().create_task(DiscordLogger.AddSentMessage(messageObject))
        return messageObject

    @staticmethod
    async def EditMessage(message, content=None, embed=None):
        await discord.Message.edit(message, content=content, embed=embed)

    @staticmethod
    async def DeleteMessage(message):
        await discord.Message.delete(message)
        DiscordLogger.TryDeleteSentMessage(message)


if __name__ == '__main__':
    print('Running script discordapi.py')