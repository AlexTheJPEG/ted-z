import lightbulb
from hikari import Intents

from .utils.opening import load_bot_settings

CONFIG = load_bot_settings()

INTENTS = Intents.ALL_UNPRIVILEGED

bot = lightbulb.BotApp(
    CONFIG["bot"]["token"],
    intents=INTENTS,
)

if __name__ == "__main__":
    bot.run()
