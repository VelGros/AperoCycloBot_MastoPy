from mastodon import Mastodon
from datetime import datetime

# AUTH
masto_auth_cfg = open("masto_auth.cfg", 'r') # Opens auth token config file
mastodon = Mastodon(access_token = masto_auth_cfg.readline(), api_base_url="masto.bike") # Login against masto.bike
masto_auth_cfg.close() # Close auth token file
Mastodon = mastodon

logs = open("AperoCycloBot.log", 'a')

# PROCESSING
try:
    # Read last stored toot ID from file
    lastToot_txt = open("lastToot.txt", 'r')
    lastToot = lastToot_txt.readline()
    lastToot_txt.close()

    # Gather ID of the last toot posted with hashtag AperoCycloParis since lastToot
    searchResult = str((Mastodon.timeline_hashtag("AperoCycloParis", local=True, since_id=lastToot))[0].id)
    logs.write(datetime.now().strftime("%d.%m.%Y %H:%M:%S")+" - Newer toot found: "+searchResult+"\n")

    # Reblog
    Mastodon.status_reblog(searchResult)

    # Write new toot ID to lastToot.txt
    lastToot_txt = open("lastToot.txt", 'w')
    lastToot_txt.write(searchResult)
    lastToot_txt.close()
    
except IndexError: 
  logs.write((datetime.now().strftime("%d.%m.%Y %H:%M:%S")+" - No new toot found \n"))

logs.close()

