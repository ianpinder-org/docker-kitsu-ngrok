import gazu
import os

from dotenv import load_dotenv

load_dotenv() 

KITSU_EVENTS_URL = os.getenv("KITSU_URL")
KITSU_EVENTS_TOKEN = os.getenv("KITSU_EVENTS_TOKEN")


gazu.set_host(f"{KITSU_EVENTS_URL}/api")
gazu.set_event_host(KITSU_EVENTS_URL)
# gazu.log_in("", "")
gazu.set_token (KITSU_EVENTS_TOKEN)



def my_callback(data):
    print("Asset created %s" % data["asset_id"])

event_client = gazu.events.init()
gazu.events.add_listener(event_client, "asset:new", my_callback)
gazu.events.run_client(event_client)