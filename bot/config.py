from environs import Env
import os

DIRNAME = os.path.dirname(__file__)
os.chdir(f"{DIRNAME}//..")

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
BOT_ADMINS = env.list("BOT_ADMINS")
DONATE_CHANNEL_ID = env.int("DONATE_CHANNEL_ID")
API_KEYS = env.list("API_KEYS")
