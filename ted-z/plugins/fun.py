import os
import random
from typing import Annotated as Atd

import crescent
import hikari

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
with open(f"{dir_path}/files/slaps.txt", 'r') as file:
    SLAPS = [line.strip() for line in file.readlines()]

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="slap", description="Slap someone")
async def slap(ctx: crescent.Context, user: Atd[hikari.User, "The person you want to slap"]) -> None:
    response = random.choice(SLAPS)

    if ctx.user.username == user.username:
        slapee = "yourself"
        slap_message = response.format(slapee)
        slap_message = slap_message.replace(" they", " you")
        slap_message = slap_message.replace(" their", " your")
        slap_message = slap_message.replace(" them", " yourself")
    elif f"{user.username}#{user.discriminator}" == "Ted#2395":
        slapee = "me"
        slap_message = response.format(slapee)
        slap_message = slap_message.replace(" they", " I")
        slap_message = slap_message.replace(" their", " my")
        slap_message = slap_message.replace(" them", " myself")
    else:
        slapee = user.username
        slap_message = response.format(slapee)

    await ctx.respond(slap_message)


def create_ground_string(groundee, reason):
    time = random.randrange(10 ** 50, 10 ** 51)
    oh = "OH" * random.randint(15, 30)
    grounded = ("GROUNDED " * random.randint(3, 9)).strip()
    time_unit = random.choice(["YEARS", "CENTURIES", "EONS", "ETERNITIES"])
    return (
        f"{oh} {groundee.upper()} HOW DARE YOU {reason.upper()}!!! "
        f"THAT'S IT. YOU ARE {grounded} FOR {time} {time_unit}!!!!!!!!!!"
    )


@plugin.include
@crescent.command(name="slap", description="Ground someone")
async def ground(ctx: crescent.Context,
                 user: Atd[hikari.User, "The person you want to ground"],
                 reason: Atd[str, "The reason you're grounding them"]) -> None:
    ground_message = create_ground_string(user.username, reason)
    await ctx.respond(ground_message)


@plugin.include
@crescent.command(name="thegame", description="You lost The Game. Now make everyone else lose it")
async def thegame(ctx: crescent.Context) -> None:
    await ctx.respond("I lost The Game.")