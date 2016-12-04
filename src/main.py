import dota2api
import json

# API key
class Client():
    def __init__(self):
        self.api = dota2api.Initialise('44D2B9F7C72B1931CC601FF4086C9014')

    # Return dict of player ids : player names from live match
    def get_players(self, matchid):
        match = self.api.get_match_details(matchid)
        data = json.loads(match.json)
        players = []
        # Should get list of players indexed by slot in game
        for i in range(len(data['players'])):
            players.append(data['players'][i]['account_id'])
        return players

    # Return hyperlink to dotabuff profile of playerid
    def get_dotabuff(self, playerid):
        data = self.api.get_player_summaries(steamids=playerid)
        if (len(data['players'])):
            return '<http://www.dotabuff.com/players/%s>\t[%s]\n' % (str(playerid), data['players'][0]['personaname'])
        else:
            return ''

    # Render links to players dotabuff profiles from live match
    def display_profiles(self, matchid):
        players = self.get_players(matchid)
        resp = "**Radiant Team**\n"
        for i in range(len(players)):
            if i == 5:
                resp = resp + "**Dire Team**\n"
            resp = resp + self.get_dotabuff(players[i])
        return resp

    def testid(self, playerid):
        # Test if playerid has exposed match data
        pass

if __name__ == '__main__':
    s = start()
    s.display_profiles(2816280827)