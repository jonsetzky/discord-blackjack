

import discord

from .hand import Hand


class Player():
    isReady = False

    # players embed displays money, hands and whether he has stood
    embedObject = None

    author = 0
    money = 0 
    hands = list()

    def __init__(self):
        self.hands = list()

        self.embedShouldUpdate = True

    def RenderHands(self):
        if len(self.hands) < 1:
            return False
        outs = ""
        for hand in self.hands:
            outs += f"$**{hand.bet}**"
            if len(hand.cards) > 0:
                outs += f" – {hand.asString()}.\n"
        return str(outs)

    # returns an array of informations strips of form
    # (HEAD, DESCRIPTION)    
    def getStateInfo(self):
        arr = list()
        arr.append(('Money', f'${self.money}'))
        
        hands = self.RenderHands()
        if hands:
            arr.append(('Hand' + (len(self.hands) > 1) * 's', hands))

        return arr

    @staticmethod
    def PlayerEmbed(player):
        embedDict = {
            'title': str(player.author.name),
            'color': 16711680,
            'fields': list()
        }
        for stateInfo in player.getStateInfo():
            embedDict['fields'].append({
                'name': stateInfo[0],
                'inline': False,
                'value': str(stateInfo[1])
            })
        return discord.Embed.from_dict(embedDict)

    def ClearHands(self):
        self.hands = list()

    """def getEmbed(self):
        fields = list()
        fields.append({
                'name': 'Money',
                'inline': False,
                'value': str(f'${self.money}\n')
        })
        hands = self.RenderHands()
        if hands:
            fields.append({
                    'name': 'Hands',
                    'inline': False,
                    'value': str(self.RenderHands())
            })

        return discord.Embed.from_dict({
            'title': str(self.name),
            'color': 16711680,
            'fields': fields
        })"""