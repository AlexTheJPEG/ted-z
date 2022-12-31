import random

import crescent

from ..utils.opening import open_file

EB_RESPONSES = open_file("eb_responses.txt")

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="8ball", description="Ask the magic 8-Ted a question")
class EightBallCommand:
    question = crescent.option(str, "The question to ask")

    async def callback(self, ctx: crescent.Context) -> None:
        response = random.choice(EB_RESPONSES)
        await ctx.respond(f':speech_balloon: "{self.question}"\n\n:8ball: {response}')


@plugin.include
@crescent.command(name="roll", description="Roll some dice")
class RollCommand:
    number = crescent.option(int, "Number of dice (default: 1)", default=1)
    sides = crescent.option(int, "Number of sides on each die (default: 6)", default=6)

    async def callback(self, ctx: crescent.Context) -> None:
        dice_notation = f"{self.number}d{self.sides}"
        dice_rolls = [random.randint(1, self.sides) for _ in range(self.number)]
        await ctx.respond(f":game_die: Rolled a {dice_notation} and got:\n\n{dice_rolls}")


@plugin.include
@crescent.command(name="coin", description="Flip a coin")
class CoinCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        if random.randint(0, 1):
            await ctx.respond(f":coin: It's heads.")
        else:
            await ctx.respond(f":coin: It's tails.")


@plugin.include
@crescent.command(name="lottery", description="Draw some lottery numbers")
class LotteryCommand:
    lottery_type = crescent.option(
        str,
        "The lottery game to choose numbers for",
        choices=(
            ("Powerball", "powerball"),
            ("Mega Millions", "megamillions"),
            ("EuroMillions", "euromillions"),
        ),
    )

    async def callback(self, ctx: crescent.Context) -> None:
        match self.lottery_type:
            case "powerball":
                # (USA) Powerball
                # Five numbers (1-69) + one powerball number (1-26)
                five_numbers = [random.randint(1, 69) for _ in range(5)]
                five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
                powerball_number = random.randint(1, 26)
                await ctx.respond(
                    ":moneybag: Here are your Powerball numbers:\n\n"
                    f"{five_numbers_formatted} **({powerball_number})**",
                    ephemeral=True,
                )
            case "megamillions":
                # (USA) Mega Millions
                # Five numbers (1-70) + one megaball number (1-25)
                five_numbers = [random.randint(1, 70) for _ in range(5)]
                five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
                megaball_number = random.randint(1, 25)
                await ctx.respond(
                    ":moneybag: Here are your Mega Millions numbers:\n\n"
                    f"{five_numbers_formatted} **({megaball_number})**",
                    ephemeral=True,
                )
            case "euromillions":
                # (EUR) EuroMillions
                # Five numbers (1-50) + two lucky star numbers (1-12)
                five_numbers = [random.randint(1, 50) for _ in range(5)]
                five_numbers_formatted = ", ".join(list(map(str, five_numbers)))
                lucky_star_numbers = [random.randint(1, 12) for _ in range(2)]
                lucky_star_numbers_formatted = " ".join(list(map(str, lucky_star_numbers)))
                await ctx.respond(
                    ":moneybag: Here are your EuroMillions numbers:\n\n"
                    f"{five_numbers_formatted} **({lucky_star_numbers_formatted})**",
                    ephemeral=True,
                )
