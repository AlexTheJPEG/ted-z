import asyncio
import random

import aiohttp
import hikari
import lightbulb
import miru

from ..utils.web import HEADERS

plugin = lightbulb.Plugin("games")

RPS_EMOTES = {"rock": "\N{ROCK}", "paper": "\N{SCROLL}", "scissors": "\N{BLACK SCISSORS}"}
RPS_WINLOSS = {
    "rock": ["scissors", "paper"],
    "paper": ["rock", "scissors"],
    "scissors": ["paper", "rock"],
}


class RPSView(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @miru.button(label="Rock", emoji="\N{ROCK}", style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.move = "rock"
        self.stop()

    @miru.button(label="Paper", emoji="\N{SCROLL}", style=hikari.ButtonStyle.PRIMARY)
    async def paper_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.move = "paper"
        self.stop()

    @miru.button(label="Scissors", emoji="\N{BLACK SCISSORS}", style=hikari.ButtonStyle.PRIMARY)
    async def scissors_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.move = "scissors"
        self.stop()

    @miru.button(emoji="\N{BLACK SQUARE FOR STOP}", style=hikari.ButtonStyle.DANGER, row=2)
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.respond("Cancelled.")
        self.stop()


class TriviaView(miru.View):
    def __init__(self, author, public, *args, **kwargs) -> None:
        self.author = author
        self.public = public
        super().__init__(*args, **kwargs)

    @miru.button(label="A", style=hikari.ButtonStyle.PRIMARY)
    async def a_button(self, button: miru.Button, ctx: miru.Context) -> None:
        if (self.public or ctx.author.id == self.author.id) and button.label is not None:
            self.answer = button.label.lower()
            self.who_clicked = ctx.user
            self.stop()

    @miru.button(label="B", style=hikari.ButtonStyle.PRIMARY)
    async def b_button(self, button: miru.Button, ctx: miru.Context) -> None:
        if (self.public or ctx.author.id == self.author.id) and button.label is not None:
            self.answer = button.label.lower()
            self.who_clicked = ctx.user
            self.stop()

    @miru.button(label="C", style=hikari.ButtonStyle.PRIMARY)
    async def c_button(self, button: miru.Button, ctx: miru.Context) -> None:
        if (self.public or ctx.author.id == self.author.id) and button.label is not None:
            self.answer = button.label.lower()
            self.who_clicked = ctx.user
            self.stop()

    @miru.button(label="D", style=hikari.ButtonStyle.PRIMARY)
    async def d_button(self, button: miru.Button, ctx: miru.Context) -> None:
        if (self.public or ctx.author.id == self.author.id) and button.label is not None:
            self.answer = button.label.lower()
            self.who_clicked = ctx.user
            self.stop()

    @miru.button(emoji="\N{BLACK SQUARE FOR STOP}", style=hikari.ButtonStyle.DANGER, row=2)
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        if ctx.author.id == self.author.id:
            await ctx.respond("Cancelled.")
            self.stop()


@plugin.command
@lightbulb.option(
    name="player",
    description="Who to play against (default: play against me!)",
    type=hikari.User,
    default=None
)
@lightbulb.command(name="rps", description="Play rock-paper-scissors", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context) -> None:
    async def player_vs_bot():
        while True:
            view = RPSView(timeout=60)
            message = await ctx.respond("Pick a move!", components=view)
            await view.start(message)
            await view.wait()
            if hasattr(view, "move"):
                game_string = f"Rock, paper, scissors, shoot!"
                game = await ctx.respond(game_string, user_mentions=True)
                await asyncio.sleep(2)

                player_move = view.move
                bot_move = random.choice(list(RPS_EMOTES.keys()))

                game_string += f"\n\n{RPS_EMOTES[player_move]} You chose {player_move}."
                await game.edit(game_string)
                await asyncio.sleep(1)

                game_string += f"\n{RPS_EMOTES[bot_move]} I chose {bot_move}."
                await game.edit(game_string)
                await asyncio.sleep(1)

                bot_wins = RPS_WINLOSS[bot_move][0]
                bot_loses = RPS_WINLOSS[bot_move][1]

                if player_move == bot_wins:
                    game_string += f"\n\n**I win!**"
                elif player_move == bot_loses:
                    game_string += f"\n\n**You win.**"
                else:
                    game_string += f"\n\n**It's a draw.**"

                await game.edit(game_string)

                if not game_string.endswith("draw.**"):
                    break

                await asyncio.sleep(1)
            else:
                break

    if ctx.options.player is None or ctx.options.player.mention == ctx.bot.get_me().mention:  # type: ignore
        await player_vs_bot()
    elif ctx.options.player.mention == ctx.author.mention:
        await ctx.respond("You can't play against yourself!")
    else:
        await ctx.respond("guh")


@plugin.command
@lightbulb.option(
    name="public",
    description="Can anyone answer the question? (default: False, only you can answer)",
    type=bool,
    default=False,
)
@lightbulb.command(name="trivia", description="Try to answer a random trivia question")
@lightbulb.implements(lightbulb.SlashCommand)
async def trivia(ctx: lightbulb.Context) -> None:
    # Get a random question
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://the-trivia-api.com/api/questions?limit=1&region=US", headers=HEADERS
        ) as response:
            question_json = (await response.json())[0]

    category = question_json["category"]
    question = question_json["question"]

    # Shuffle the answers
    correct_answer = question_json["correctAnswer"].strip()
    answers = [answer.strip() for answer in question_json["incorrectAnswers"] + [correct_answer]]
    random.shuffle(answers)

    # Correspond each answer with a letter
    answers_with_letters = {chr(97 + i): answers[i] for i in range(len(answers))}
    correct_answer_letter = chr(97 + answers.index(correct_answer))

    answers_list = [f":regional_indicator_{k}: {v}" for k, v in answers_with_letters.items()]
    answers_string = "\n".join(answers_list)
    trivia_string = [f"**Category: {category}**", question, answers_string]

    view = TriviaView(ctx.author, ctx.options.public, timeout=60)
    message = await ctx.respond("\n\n".join(trivia_string), components=view)
    await view.start(message)
    await view.wait()

    if hasattr(view, "answer"):
        # Indicate the right answer with a check mark
        answers_list[answers.index(correct_answer)] += " :white_check_mark:"

        if answers_with_letters[view.answer] == correct_answer:
            await ctx.respond(f"{view.who_clicked.mention} That is correct!", user_mentions=True)
        else:
            await ctx.respond(
                (
                    f"{view.who_clicked.mention} That is incorrect. The answer was:"
                    f" :regional_indicator_{correct_answer_letter}: {correct_answer}."
                ),
                user_mentions=True,
            )
            # Mark the user's answer with an X
            answers_list[answers.index(answers_with_letters[view.answer])] += " :x:"

        answers_string = "\n".join(answers_list)
        trivia_string = [f"**Category: {category}**", question, answers_string]
        await message.edit("\n\n".join(trivia_string))


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
