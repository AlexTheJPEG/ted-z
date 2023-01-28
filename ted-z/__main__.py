import lightbulb
import miru
from hikari import Intents

from .utils.opening import load_bot_settings

CONFIG = load_bot_settings()

INTENTS = Intents.ALL_UNPRIVILEGED | Intents.MESSAGE_CONTENT

bot = lightbulb.BotApp(
    CONFIG["bot"]["token"],
    intents=INTENTS,
    prefix="$",
)

if __name__ == "__main__":
    bot.load_extensions_from("./ted-z/plugins/")
    miru.install(bot)
    bot.run()
