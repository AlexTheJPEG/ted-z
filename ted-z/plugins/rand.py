import random

from hikari import CommandChoice
import lightbulb

from ..utils.opening import open_file

EB_RESPONSES = open_file("eb_responses.txt")

plugin = lightbulb.Plugin("rand")


@plugin.command
@lightbulb.option(name="question", description="The question to ask", type=str)
@lightbulb.command(name="8ball", description="Ask the magic 8-Ted a question")
@lightbulb.implements(lightbulb.SlashCommand)
async def eight_ball(ctx: lightbulb.Context) -> None:
    response = random.choice(EB_RESPONSES)
    await ctx.respond(f':speech_balloon: "{ctx.options.question}"\n\n:8ball: {response}')


@plugin.command
@lightbulb.option(
    name="number",
    description="Number of dice (default: 1)",
    type=int,
    default=1,
    min_value=1,
    max_value=100,
)
@lightbulb.option(
    name="sides",
    description="Number of sides on each die (default: 6)",
    type=int,
    default=6,
    min_value=2,
    max_value=100,
)
@lightbulb.command(name="roll", description="Roll some dice")
@lightbulb.implements(lightbulb.SlashCommand)
async def roll(ctx: lightbulb.Context) -> None:
    dice_notation = f"{ctx.options.number}d{ctx.options.sides}"
    dice_rolls = [random.randint(1, ctx.options.sides) for _ in range(ctx.options.number)]
    await ctx.respond(f":game_die: Rolled a {dice_notation} and got:\n\n{dice_rolls}")


@plugin.command
@lightbulb.command(name="coin", description="Flip a coin")
@lightbulb.implements(lightbulb.SlashCommand)
async def coin(ctx: lightbulb.Context) -> None:
    if random.randint(0, 1):
        await ctx.respond(f":coin: It's heads.")
    else:
        await ctx.respond(f":coin: It's tails.")


@plugin.command
@lightbulb.option(
    name="lottery_type",
    description="The lottery game to choose numbers for",
    choices=(
        CommandChoice(name="Powerball", value="powerball"),
        CommandChoice(name="Mega Millions", value="megamillions"),
        CommandChoice(name="EuroMillions", value="euromillions"),
    ),
)
@lightbulb.command(name="lottery", description="Draw some lottery numbers", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def lottery(ctx: lightbulb.Context) -> None:
    if ctx.options.lottery_type == "powerball":
        # (USA) Powerball
        # Five numbers (1-69) + one powerball number (1-26)
        five_numbers = [str(random.randint(1, 69)) for _ in range(5)]
        five_numbers_formatted = ", ".join(five_numbers)
        powerball_number = random.randint(1, 26)
        await ctx.respond(
            ":moneybag: Here are your Powerball numbers:\n\n"
            f"{five_numbers_formatted} **({powerball_number})**"
        )
    elif ctx.options.lottery_type == "megamillions":
        # (USA) Mega Millions
        # Five numbers (1-70) + one megaball number (1-25)
        five_numbers = [str(random.randint(1, 70)) for _ in range(5)]
        five_numbers_formatted = ", ".join(five_numbers)
        megaball_number = random.randint(1, 25)
        await ctx.respond(
            ":moneybag: Here are your Mega Millions numbers:\n\n"
            f"{five_numbers_formatted} **({megaball_number})**"
        )
    elif ctx.options.lottery_type == "euromillions":
        # (EUR) EuroMillions
        # Five numbers (1-50) + two lucky star numbers (1-12)
        five_numbers = [str(random.randint(1, 50)) for _ in range(5)]
        five_numbers_formatted = ", ".join(five_numbers)
        lucky_star_numbers = [str(random.randint(1, 12)) for _ in range(2)]
        lucky_star_numbers_formatted = " ".join(lucky_star_numbers)
        await ctx.respond(
            ":moneybag: Here are your EuroMillions numbers:\n\n"
            f"{five_numbers_formatted} **({lucky_star_numbers_formatted})**"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
