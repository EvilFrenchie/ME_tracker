import requests
from loguru import logger
import argparse
import asyncio
import discord
from discord.ext import commands

#command line parameters (temp until better solution)
parser = argparse.ArgumentParser(description='pricebot settings.  channel,guild,frequency args optional to provide regular updates to a single channel')
parser.add_argument('--token', dest='discord_token', required=True)
parser.add_argument('--guild', dest='discord_guild', required=False)
parser.add_argument('--channel', dest='discord_channel', required=False)
parser.add_argument('--frequency', dest='freq',  required=False,
                    help='frequency to check price in SECONDS')
parser.add_argument('--log', dest='log_level',  default='INFO',
                    help='frequency to check price in SECONDS')      
args= parser.parse_args()

#Initialize logger
logger.add("./logs/log_{time}.log", format="{time} {level} {message}", level=args.log_level, rotation="20 MB")
logger.info("ME TRACKER DISCORD BOT")

#to store the current version of the price embed to send to the discord client
summary_embed = None
new_collections_embed = None

#discord client connection 
## need to do some reading on async...
#client = discord.Client()
client = commands.Bot( command_prefix="!" )

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!summary':
        await message.channel.send(embed=summary_embed)   

    if message.content == '!new':
        await message.channel.send(embed=new_collections_embed)

#only runs the channel update loop if all three of these values are provided as args
# discord_guild, discord_channel, frequency
#this is dumb, replace with a proper
async def periodic_channel_updates(freq,input_guild,input_channel):
    while True: 
        if(len(client.guilds) > 0):
            for guild in client.guilds:
                if guild.name == input_guild:
                    logger.debug(f'Belongs to guild: {guild}')
                    
                    for channel in guild.channels:
                        if channel.name == input_channel:
                            logger.debug(f'Belongs to channel: {channel}')

                            #pamp it
                            await channel.send(embed=summary_embed)
                
        await asyncio.sleep(int(freq))


#refreshes price & volume info from dexlab once every 60 seconds
#probably need to update this to be more async friendly (in the requests.get s)
async def data_refresh():
    while True:
        #load latest data from trader_bot_stats file here??

      

        #calculate % change of price over 24 hours
        price_change_24h = 0.0
        if current_price > price_24h_ago:
            price_change_24h = ((current_price-price_24h_ago)/price_24h_ago)*100  
            percent_color = discord.Color.green() 
        elif price_24h_ago > current_price:
            price_change_24h = -(((price_24h_ago - current_price)/price_24h_ago)*100)
            percent_color = discord.Color.red() 
        else:
            price_change_24h = 0.0


        #print data to log
        logger.info("Current price: " + str(round(current_price,6)))
        logger.info("Price 24hr Ago: " + str(round(price_24h_ago,6)))
        logger.info("24hr Volume: " + str(round(volume_24h,2)))
        logger.info("24hr Price Change: " + str(round(price_change_24h,2)) + "%")

        #Create discord embed thing
        temp_embed = discord.Embed(title="Price Check! ", color=discord.Color.green())
        temp_embed.add_field(name="**Current Price**", value=f'${str(round(current_price,6))} USDC', inline=False)
        temp_embed.add_field(name="**Price % Change (24h)**", value=f'{str(round(price_change_24h,2))}% ', inline=True)
        temp_embed.add_field(name="**24 Hour Volume**", value=f'${str(round(volume_24h,2))} USDC', inline=False)
        temp_embed.set_footer(text="All values via dexlabs")

        #update the global price embed data
        global summary_embed
        summary_embed = temp_summary_embed

        #update the global collections embed ddata
        global new_collections_embed
        new_collections_embed = temp_collections_embed

        #sleep 30 seconds & do it all over again
        await asyncio.sleep(60)


#run discord client loop

#only runs the channel update loop if all three of these values are provided
if args.freq and args.discord_guild and args.discord_channel:
    client.loop.create_task(periodic_channel_updates(args.freq,args.discord_guild,args.discord_channel))

client.loop.create_task(dexlab_data_refresh())
client.run(args.discord_token)

