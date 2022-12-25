import random

from ..utils.opening import open_file, load_bot_settings

import crescent
import hikari
import requests

SLAPS = open_file("slaps.txt")

config = load_bot_settings()
BOT_USERNAME = config["bot"]["username"]

plugin = crescent.Plugin()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/plain",
}


@plugin.include
@crescent.command(name="slap", description="Slap someone")
class SlapCommand:
    user = crescent.option(hikari.User, "The person you want to slap")

    async def callback(self, ctx: crescent.Context) -> None:
        response = random.choice(SLAPS)

        if ctx.user.username == self.user.username:
            slapee = "yourself"
            slap_message = response.format(slapee)
            slap_message = slap_message.replace(" they", " you")
            slap_message = slap_message.replace(" their", " your")
            slap_message = slap_message.replace(" them", " yourself")
        elif f"{self.user.username}#{self.user.discriminator}" == BOT_USERNAME:
            slapee = "me"
            slap_message = response.format(slapee)
            slap_message = slap_message.replace(" they", " I")
            slap_message = slap_message.replace(" their", " my")
            slap_message = slap_message.replace(" them", " myself")
        else:
            slapee = self.user.mention
            slap_message = response.format(slapee)

        await ctx.respond(slap_message)


@plugin.include
@crescent.command(name="ground", description="Ground someone")
class GroundCommand:
    user = crescent.option(hikari.User, "The person you want to ground")
    reason = crescent.option(str, "The reason you're grounding them")

    def create_ground_string(self, groundee, reason):
        time = random.randrange(10**50, 10**51)
        oh = "OH" * random.randint(15, 30)
        grounded = ("GROUNDED " * random.randint(3, 9)).strip()
        time_unit = random.choice(["YEARS", "CENTURIES", "EONS", "ETERNITIES"])
        return (
            f"{oh} {groundee.upper()} HOW DARE YOU {reason.upper()}!!! "
            f"THAT'S IT. YOU ARE {grounded} FOR {time} {time_unit}!!!!!!!!!!"
        )

    async def callback(self, ctx: crescent.Context) -> None:
        ground_message = self.create_ground_string(self.user.mention, self.reason)
        await ctx.respond(ground_message)


@plugin.include
@crescent.command(
    name="thegame", description="You lost The Game. Now make everyone else lose it"
)
class TheGameCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.respond("I lost The Game.")


@plugin.include
@crescent.command(name="joke", description="Tell a random joke")
class JokeCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        response = requests.get("https://icanhazdadjoke.com/", headers=HEADERS)
        await ctx.respond(response.content.decode("utf-8"))
