import random

import aiohttp
import hikari
import lightbulb

from ..utils.opening import open_file
from ..utils.web import HEADERS

SLAPS = open_file("slaps.txt")

plugin = lightbulb.Plugin("fun")


@plugin.command
@lightbulb.option(name="user", description="The person you want to slap", type=hikari.User)
@lightbulb.command(name="slap", description="Slap someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def slap(ctx: lightbulb.Context) -> None:
    response = random.choice(SLAPS)
    user = ctx.options.user

    # If the user chooses to slap themself
    if user.id == ctx.author.id:
        slapee = "yourself"
        slap_message = response.format(slapee)
        slap_message = slap_message.replace(" they", " you")
        slap_message = slap_message.replace(" their", " your")
        slap_message = slap_message.replace(" them", " yourself")
    # If the user chooses to slap Ted
    elif (bot_user := ctx.bot.get_me()) is not None and user.id == bot_user.id:
        slapee = "me"
        slap_message = response.format(slapee)
        slap_message = slap_message.replace(" they", " I")
        slap_message = slap_message.replace(" their", " my")
        slap_message = slap_message.replace(" them", " me")
    # If the user chooses to slap anyone else
    else:
        slapee = user.mention
        slap_message = response.format(slapee)

    await ctx.respond(slap_message, user_mentions=True)


def create_ground_string(groundee: str, reason: str) -> str:
    time = random.randrange(10**50, 10**51)
    oh = "OH" * random.randint(15, 30)
    grounded = ("GROUNDED " * random.randint(3, 9)).rstrip()
    time_unit = random.choice(["YEARS", "CENTURIES", "EONS", "ETERNITIES"])
    return (
        f"{oh} {groundee.upper()} HOW DARE YOU {reason.upper()}!!! "
        f"THAT'S IT. YOU ARE {grounded} FOR {time} {time_unit}!!!!!!!!!!"
    )


@plugin.command
@lightbulb.option(
    name="reason",
    description='The reason you\'re grounding them (Fill in the blank: "HOW DARE YOU _____!!!")',
    type=str,
)
@lightbulb.option(name="user", description="The person you want to ground", type=hikari.User)
@lightbulb.command(name="ground", description="Ground someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def ground(ctx: lightbulb.Context) -> None:
    ground_message = create_ground_string(ctx.options.user.mention, ctx.options.reason)
    await ctx.respond(ground_message, user_mentions=True)


@plugin.command
@lightbulb.command(name="thegame", description="You lost The Game. Now make everyone else lose it")
@lightbulb.implements(lightbulb.SlashCommand)
async def thegame(ctx: lightbulb.Context) -> None:
    await ctx.respond("I lost The Game.")


@plugin.command
@lightbulb.command(name="joke", description="Tell a random joke")
@lightbulb.implements(lightbulb.SlashCommand)
async def joke(ctx: lightbulb.Context) -> None:
    headers = HEADERS
    headers["Accept"] = "text/plain"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://icanhazdadjoke.com", headers=headers) as response:
            joke_text = await response.text(encoding="utf-8")

    await ctx.respond(joke_text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
