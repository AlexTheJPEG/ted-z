import random
from typing import Annotated as Atd

import crescent
import dice
import eight_ball
import hikari

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="8ball", description="Ask the magic 8-Ted a question")
async def eightball(ctx: crescent.Context, question: Atd[str, "The question to ask (must end in '?')"]) -> None:
    ball = eight_ball.ball()
    if question[-1] == '?':
        await ctx.respond(f":speech_balloon: \"{question}\"\n\n:8ball: {ball.response(question)}")
    else:
        await ctx.respond("Your question must end in '?'.")


@plugin.include
@crescent.command(name="roll", description="Roll some dice")
async def roll(ctx: crescent.Context,
               number: Atd[int, "Number of dice (default: 1)", crescent.MaxValue(100),] | None = 1,
               sides: Atd[int, "Number of sides on each die (default: 6)", crescent.MaxValue(100)] | None = 6) -> None:
    dice_notation = f"{number}d{sides}"
    await ctx.respond(f":game_die: Rolled a {dice_notation} and got:\n\n{dice.roll(dice_notation)}")


@plugin.include
@crescent.command(name="coin", description="Flip a coin")
async def coin(ctx: crescent.Context) -> None:
    if random.randint(0, 1):
        await ctx.respond(f":coin: It's heads.")
    else:
        await ctx.respond(f":coin: It's tails.")


@plugin.include
@crescent.command(name="lottery", description="Draw some lottery numbers")
async def lottery(ctx: crescent.Context,
                  lottery_type: Atd[
                      str,
                      crescent.Choices(
                          hikari.CommandChoice(name="Powerball", value="powerball"),
                          hikari.CommandChoice(name="Mega Millions", value="megamillions"),
                          hikari.CommandChoice(name="EuroMillions", value="euromillions"),
                      ),
                  ]) -> None:
    match lottery_type:
        case "powerball":
            # (USA) Powerball
            # Five numbers (1-69) + one powerball number (1-26)
            five_numbers = [random.randint(1, 69) for _ in range(5)]
            five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
            powerball_number = random.randint(1, 26)
            await ctx.respond(
                ":moneybag: Here are your Powerball numbers:"
                f"\n\n{five_numbers_formatted} **({powerball_number})**",
                ephemeral=True
            )
        case "megamillions":
            # (USA) Mega Millions
            # Five numbers (1-70) + one megaball number (1-25)
            five_numbers = [random.randint(1, 70) for _ in range(5)]
            five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
            megaball_number = random.randint(1, 25)
            await ctx.respond(
                ":moneybag: Here are your Mega Millions numbers:"
                f"\n\n{five_numbers_formatted} **({megaball_number})**",
                ephemeral=True
            )
        case "euromillions":
            # (EUR) EuroMillions
            # Five numbers (1-50) + two lucky star numbers (1-12)
            five_numbers = [random.randint(1, 50) for _ in range(5)]
            five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
            lucky_star_numbers = [random.randint(1, 12) for _ in range(2)]
            lucky_star_numbers_formatted = " ".join(list(map(str, lucky_star_numbers)))
            await ctx.respond(
                ":moneybag: Here are your EuroMillions numbers:"
                f"\n\n{five_numbers_formatted} **({lucky_star_numbers_formatted})**",
                ephemeral=True
            )
