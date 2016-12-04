

import json
import dota2api

class Client():

    def __init__(self):
        self.players = {}
        self.key = None
        self.data = dota2api.Initialise('44D2B9F7C72B1931CC601FF4086C9014')

        # Attempt to load existing player list from file
        try:
            with open("data/players.json","r") as file:
                self.players = json.load(file)
            with open("data/key.json","r") as file:
                self.key = json.load(file)

        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            if e.filename == "data/players.json":
                with open("data/players.json","w") as file:
                    json.dump(self.players, file)
            else:
                print(e.strerror)
        file.close()

    def last(self, player):
        ''' Returns a list of the stats from the players most recent match [[stats], [result], [heroid]]'''
        matchid = self.data.get_match_history(account_id=self.getid(player), matches_requested=1)['matches'][0]['match_id']
        return '<http://www.dotabuff.com/matches/' + str(matchid)+'>'

    def set(self, alias, playerid):
        ''' Sets the alias (name) for the provided playerid; also used to add players '''
        self.players[alias] = playerid
        self.save()
        return 'Player added.'

    def delete(self, playerid):
        ''' Removes player from the dict with the current playerid '''
        try:
            self.players.__delitem__(str(playerid))
        except KeyError as e:
            return 'Player not found.'
        self.save()
        return 'Delete playerid alias'

    def show(self):
        ''' Lists current alias '''
        return self.players
    
    def save(self):
        ''' Save changes to alias list '''
        with open("data/players.json","w") as file:
            json.dump(self.players, file)
        
    def getid(self, player):
        ''' Returns player id from alias '''
        return self.players.get(player)
        