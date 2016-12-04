import discord
import main
import players
import re
import json

with open json('data/key.json','r') as file:
    key = json.loads(file)[0]
client = discord.Client()
players = players.Client()
main = main.Client()

@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    regex = r'![a-z]+'
    print(re.search(regex, message.content))
    if re.search(regex, message.content):
        data = message.content.split()
        print(data)
        if data[0] == '!lm':
            resp = players.last(data[1])
        if data[0] == '!players':
            pd = players.show()
            resp = ''
            for n in pd:
                resp = resp + '[%s]\t<http://www.dotabuff.com/players/%s>\n' % (n, pd[n])
        if data[0] == '!delete':
            resp = players.delete(data[1])
        if data[0] == '!add':
            resp = players.set(data[1], data[2])
        if data[0] == '!help':
            resp = '!lm playername\n!players\n!delete playername\n!add playername accountid\n!help'
        if data[0] == '!test':
            resp = main.display_profiles(2818489700)
        await client.send_message(message.channel, resp)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(key)