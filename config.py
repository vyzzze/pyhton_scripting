from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
NICK = os.getenv("NICK")
CHANNEL = os.getenv("CHANNEL")
PREFIX = os.getenv("PREFIX")
OBS_HOST = os.getenv("OBS_HOST")
OBS_PORT = int(os.getenv("OBS_PORT"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")
SCENE_NAME = os.getenv("SCENE_NAME")
MOVE_IN_FILTER = os.getenv("MOVE_IN_FILTER")
MOVE_OUT_FILTER = os.getenv("MOVE_OUT_FILTER")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

#print("Twitch:", TOKEN, NICK, CHANNEL, TWITCH_USERNAME, PREFIX, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, " / OBS:", OBS_HOST, OBS_PORT, OBS_PASSWORD, SCENE_NAME, MOVE_IN_FILTER, MOVE_OUT_FILTER, "/ Discord:" , DISCORD_WEBHOOK_URL)