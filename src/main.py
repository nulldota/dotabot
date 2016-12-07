import dota2api
import json
import re

class start():
    def __init__(self):
        with open('data/key.json','r') as file:
            key = json.load(file)[1]
        self.api = dota2api.Initialise(key)
        self.location = 'server_log.txt'
    # Return dict of player ids : player names from live match

    def get_players(self):
        with open(self.location,'r') as file:
            data = file.read().split()
        data.reverse()
        for i in range(len(data)):
            if r'9:[U:1:' in data[i]:
                datastr = ''.join(data[i:i+10])
                return re.findall(r'[0-9]{8,9}',datastr) 

    # Return hyperlink to dotabuff profile of playerid
    def get_dotabuff(self, playerid):
        data = self.api.get_player_summaries(steamids=int(playerid))
        if (len(data['players'])):
            return '<http://www.dotabuff.com/players/%s>\t[%s]\n' % (str(playerid), data['players'][0]['personaname'])
        else:
            return ''

    # Render links to players dotabuff profiles from live match
    def display_profiles(self, players):
        resp = "**Radiant Team**\n"
        players.reverse()
        for i in range(len(players)):
            if i == 5:
                resp = resp + "**Dire Team**\n"
            resp = resp + self.get_dotabuff(players[i])
        return resp

    def run(self):
        players = self.get_players()
        return self.display_profiles(players)


if __name__ == '__main__':
    s = start()
    s.run()