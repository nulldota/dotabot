import dota2api
import json
import re


# Make this return separate response for radiant and dire
# Lookup function for acronyms


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
        with open(self.location,'r') as fd:
            data = fd.read().split()
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
            name = data['players'][0]['personaname']
            url = 'http://www.dotabuff.com/players/' + str(playerid)
            resp = '[{0}] ({1})\n```'.format(name, url)
            for n in range(5): # n matches
                match = self.api.get_match_details(history['matches'][n]['match_id'])
                for i in range(len(match['players'])):
                    if match['players'][i]['account_id'] == int(playerid):
                        slot = match['players'][i]
                        win = 'L'
                        if match['radiant_win'] != (i > 4):
                            win = 'W'
                        hero = '[{0}]'.format(self.resolvehero(slot['hero_id'])[0:16])
                        gpm = int(slot['gold_per_min'])
                        xpm = int(slot['xp_per_min'])
                        k = slot['kills']
                        d = slot['deaths']
                        a = slot['assists']
                        resp += '[{0}] {1:18s} [{2}:{3}] [{4:02d}:{5:02d}:{6:02d}]\n'.format(win, hero, gpm, xpm, k, d, a)
            resp += '```\n'
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