#TWITCH COMMANDS AND NOTIFICATIONS script.
from twitchio.ext import commands
from obswebsocket import obsws, requests
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from discord_webhook import DiscordWebhook
import random
import asyncio
import pyttsx3
import time
import threading
import keyboard
import sys




# === CONFIG (.env) ===
from config import(
    TOKEN,
    NICK,
    CHANNEL,
    TWITCH_USERNAME,
    PREFIX,
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    OBS_HOST,
    OBS_PORT,
    OBS_PASSWORD,
    SCENE_NAME,
    MOVE_IN_FILTER,
    MOVE_OUT_FILTER,
    DISCORD_WEBHOOK_URL
    )
# === CONFIG (.env) ===






# === OBS CONTROL ===
class OBSController:
    def __init__(self, host, port, password):
        self.ws = obsws(host, port, password)
        self.ws.connect()
    
    def trigger_scene_filter(self, scene_name, filter_name):
        self.ws.call(requests.SetSourceFilterVisibility(
            sourceName=scene_name,
            filterName=filter_name,
            filterEnabled=True
        ))

     
    def cleanup(self):
        self.ws.disconnect()
# === OBS CONTROL ===




# === TTS CONTROL ===
class TTSController:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.finished = False
        self.engine.connect('finished-utterance', self.on_tts_finished)

    def on_tts_finished(self, name, completed):
        self.finished = True

    def speak(self, text):
        self.finished = False
        self.engine.say(text)
        self.engine.runAndWait()
# === TTS CONTROL ===



# === LIVE NOTIF ===
def send_discord_live_notification():
    print("Sending Discord notification.")
    webhook = DiscordWebhook(
        url=DISCORD_WEBHOOK_URL,
        content=f"{TWITCH_USERNAME} ist live! joined hier: https://twitch.tv/{TWITCH_USERNAME} ||@everyone||"
    )
    webhook.execute()


async def check_stream_and_notify():
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    user_id = None

    async for user in twitch.get_users(logins=[TWITCH_USERNAME]):
        user_id = user.id
        break

    was_live = False

    while True:
        streams = []
        async for stream in twitch.get_streams(user_id=user_id):
            streams.append(stream)

        stream = streams[0] if streams else None

        if stream and not was_live:
            print("Stream is LIVE!")
            send_discord_live_notification()
            was_live = True
        elif not stream and was_live:
            print("Stream is offline.")
            was_live = False

        await asyncio.sleep(15)  # check every x seconds
# === LIVE NOTIF ===






# === TWITCH BOT/COMMANDS ===
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN, prefix=PREFIX, initial_channels=[CHANNEL])
        self.tts = TTSController()
        self.obs = OBSController(OBS_HOST, OBS_PORT, OBS_PASSWORD)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
    
    async def event_message(self, message):                             # ==== TWITCH CHAT COMMANDS =====
        if message.echo:
            return

        if message.content.startswith('!tts'):
            # if random.random() < 0.1:                   # 10% chance
                tts_text = message.content[5:].strip()
                print(f"[TTS Trigger] {message.author.name}: '{tts_text}'")

                # Move in
                self.obs.trigger_scene_filter(SCENE_NAME, MOVE_IN_FILTER)

                # speak
                self.tts.speak(tts_text)

                # tts ends, move out
                self.obs.trigger_scene_filter(SCENE_NAME, MOVE_OUT_FILTER)
            # else:
            #     print("[TTS Skipped - Not in 10% chance]")
    
        if message.content.startswith('!dc'):
            print(f"[Discord Trigger] {message.author.name}")
            await message.channel.send(f'@{message.author.name}, join den discord: https://dsc.gg/vyze')

        if message.content.startswith('!socials'):
            print(f"[Socials Trigger] {message.author.name}")
            await message.channel.send(f'@{message.author.name}, hier sind meine socials: https://linktr.ee/vyze')
        
        if message.content.startswith('!testlive') and message.author.name.lower() == TWITCH_USERNAME.lower():
            print("[Manual Stream Notification Triggered]")
            send_discord_live_notification()
            print("✅ Simulated live notification sent to Discord.")


    
    def shutdown(self):
        self.obs.cleanup()
# === TWITCH BOT/COMMANDS ===


    
# === MAIN ===
def listen_for_exit():
    print("Press Ctrl+C to stop script...")
    keyboard.read_event()
    sys.exit()

threading.Thread(target=listen_for_exit, daemon=True).start()

async def main():
    bot = Bot()
    await asyncio.gather(
        bot.start(),
        check_stream_and_notify()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down...')