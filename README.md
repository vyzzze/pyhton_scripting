# streaming scripts repository

this repository contains my collection of python scripts and related files that i use for my live streaming setup. these scripts handle various tasks such as twitch chat text-to-speech, obs scene control, and discord webhook integrations.

## contents

- twitch bot scripts  
- obs websocket automation
- automatic discord webhook ping (you need to figure this out yourself) [server only]
- configuration files (with sensitive data excluded)  

## important

- **sensitive credentials and tokens are stored separately** in environment files (`.env`) which are **not included** in this repository for security reasons.  
- make sure to create your own `.env` file with the necessary keys and tokens before running any scripts.
- `test.py` is for finding out your local tts voices installed 

## usage

1. clone the repository.  
2. create a `.env` file based on the `.env.example` template (if provided).  
3. install required python packages which are:
  - `twitchio` (which i believe has `asyncio` already included)
  - `obswebsocket`
  - `twitchapi`
  - `discord_webhook`
  - `pyttsx3`
  - `keyboard`
  - `python-dotenv`
4. run the scripts in a cmd window or in your environment terminal before streaming.

---

