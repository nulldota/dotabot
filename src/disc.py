import discord, re, json, time
import main, players

with open('data/key.json','r') as file:
    key = json.load(file)[0]

client = discord.Client()
players = players.Client()
main = main.start()


@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    regex = r'![a-z]+'

    if re.search(regex, message.content):
        data = message.content.split()
        user = message.author.name

        # last match !lm name
        if data[0] == '!lm' and len(data) == 1:
            resp = players.last(user)
            
        if data[0] == '!lm' and len(data) == 2:
            resp = players.last(data[1])

        # lists player aliases
        if data[0] == '!players':
            pd = players.show()
            resp = ''
            for n in pd:
                resp = resp + '[%s]\t<http://www.dotabuff.com/players/%s>\n' % (n, pd[n])
        
        # removes player alias !delete
        if data[0] == '!delete':
            resp = players.delete(user)

        # adds player alias !add id
        if data[0] == '!add':
            resp = players.set(user, data[1])

        # lists commands
        if data[0] == '!help':
            resp = '!lm\n!players\n!delete playername\n!add accountid (players add themselves)\n!help'
        
        # Captures playerlist from server_log and displays links to dotabuff
        if data[0] == '!get':
            init = time.time()
            await client.send_message(message.channel, 'Acquiring match data')
            await client.send_message(message.channel, main.run())
            resp = 'Response time: {:.2f}s'.format(time.time() - init)

        
        await client.send_message(message.channel, resp)
        
        



@client.event
async def on_ready():
    print('Login successful')


client.run(key)