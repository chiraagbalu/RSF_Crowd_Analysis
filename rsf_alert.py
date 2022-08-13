from requests_html import AsyncHTMLSession
from discord import Webhook, RequestsWebhookAdapter
import config
import asyncio, nest_asyncio

# DISCORD WEBHOOK SETUP

# set up webhook using the url in config.py (not given in repo - private data)
webhook = Webhook.from_url(config.webhookurl, adapter=RequestsWebhookAdapter())
# send test message to url
#webhook.send("Hello World")

# url to read from: this is where RSF crowd meter reads from i believe its an API endpoint
rsf_url = 'https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e'

nest_asyncio.apply()

# new session for html
session = AsyncHTMLSession()

# writes data, infinite loop
# planning to daemonize this code to run forever on an EC2 instance or something
# would also like to not have to host it in some random df

# todo: make the bot send alerts to separate roles using discord webhook
# different roles for different threshold/timeout values
# currently only one setting
# better messages

# another idea: use regression or smth to predict rsf crowd for the next 15/30min

# todo: time check, don't send alerts when the RSF isn't open


async def sendAlert(timeout=900, threshold=50):

    # running loop
    while True:
        # get url of html page to load
        r = await session.get(rsf_url)
        # render the page, let it load (sleep = 5)
        await r.html.arender(sleep=5)
        # look at the spot we need the data from
        info = r.html.find('div.styles_fullness__rayxl')
        # reads as list of elements, translate to text
        newlist = [item.text for item in info]
        # error catch if there's nothing there
        if len(newlist) == 0:
            # send alert if smth wrong w data
            webhook.send('no data')
            continue
        # get the number from the thing
        result = int(newlist[0].split('%')[0])
        # condition for sending different messages
        if result > threshold:
            webhook.send(
                f'rsf fullness above threshold of {threshold}%: maybe wait a bit')
            webhook.send(f'rsf is {result}% full')
        else:
            # webhook.send(f'@everyone')
            webhook.send(
                f'rsf fullness below threshold of {threshold}%: go now!')
            webhook.send(f'rsf is {result}% full')

        # wait extra time: in seconds
        await asyncio.sleep(timeout)

async def main():
    await asyncio.gather(
        sendAlert(timeout=30),
        sendAlert(timeout=60),
    )

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

# figure out what to do about writing to database and stuff lol
# probably write to postgres or smth and then have data analysis w pandas/matplotlib/smth pretty -> host analysis using some frontend stuff for a cute website

