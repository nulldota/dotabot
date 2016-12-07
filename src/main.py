import dota2api
import json
import re

class start():
    def __init__(self):
        with open('data/key.json','r') as file:
            key = json.load(file)[1]
        with open('../ref/heroes.json', 'r') as file:
            self.heroes = json.load(file)
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
        # Get player summary
        data = self.api.get_player_summaries(steamids=int(playerid))
        try:
            history = self.api.get_match_history(account_id=int(playerid))
            # Format string resp
            resp = '[' + data['players'][0]['personaname'] + ']'
            resp += '(http://www.dotabuff.com/players/' + str(playerid) + ')\n```'
            for n in range(3): # n matches
                match = self.api.get_match_details(history['matches'][n]['match_id'])
                for i in range(len(match['players'])):
                    if match['players'][i]['account_id'] == int(playerid):
                        slot = match['players'][i]
                        if match['radiant_win'] != (i > 4):
                            resp += '[W]   '
                        else:
                            resp += '[L]   '
                        resp += '[' + self.resolvehero(slot['hero_id']) + ']\t'
                        resp += '[GPM: ' + str(slot['gold_per_min']) + '] [XPM: ' + str(slot['xp_per_min']) + ']\t'
                        resp += '[K: ' + str(slot['kills']) + '] [D: ' + str(slot['deaths']) + '] [A: ' + str(slot['assists']) + ']\n'
            resp += '```'
            return resp
        except dota2api.src.exceptions.APIError:
            return ''

    

    # Render links to players dotabuff profiles from live match
    def display_profiles(self, players):
        resp = "**Radiant Team**\n"
        players.reverse()
        for i in range(len(players)):
            if i == 5:
                resp = resp + "**Dire Team**\n"
            resp = resp + self.get_dotabuff(players[i]) + ''
        return resp

    def run(self):
        players = self.get_players()
        return self.display_profiles(players)
    
    def resolvehero(self, heroid):
        for i in range(len(self.heroes['heroes'])):
            if self.heroes['heroes'][i]['id'] == heroid:
                return self.heroes['heroes'][i]['localized_name']
            


if __name__ == '__main__':
    s = start()
    print(s.run())
    