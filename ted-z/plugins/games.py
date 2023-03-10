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
    def __init__(self, player: hikari.User, *args, **kwargs) -> None:
        self.player = player
        super().__init__(*args, **kwargs)

    def button_check(self, button: miru.Button, ctx: miru.Context) -> None:
        if ctx.author.id == self.player.id and button.label is not None:
            self.move = button.label.lower()
            self.stop()

    @miru.button(label="Rock", emoji="\N{ROCK}", style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(label="Paper", emoji="\N{SCROLL}", style=hikari.ButtonStyle.PRIMARY)
    async def paper_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(label="Scissors", emoji="\N{BLACK SCISSORS}", style=hikari.ButtonStyle.PRIMARY)
    async def scissors_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(
        label="Cancel", emoji="\N{BLACK SQUARE FOR STOP}", style=hikari.ButtonStyle.DANGER, row=2
    )
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.button_check(button, ctx)


class RPSAcceptView(miru.View):
    def __init__(self, player: hikari.User, *args, **kwargs) -> None:
        self.player = player
        super().__init__(*args, **kwargs)

    def button_check(self, button: miru.Button, ctx: miru.Context) -> None:
        if ctx.author.id == self.player.id and button.label is not None:
            self.option = button.label.lower()
            self.stop()

    @miru.button(
        label="Accept", emoji="\N{WHITE HEAVY CHECK MARK}", style=hikari.ButtonStyle.SUCCESS
    )
    async def accept_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(
        label="Decline", emoji="\N{NEGATIVE SQUARED CROSS MARK}", style=hikari.ButtonStyle.DANGER
    )
    async def decline_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)


class TriviaView(miru.View):
    def __init__(self, author: hikari.User, public: bool, *args, **kwargs) -> None:
        self.author = author
        self.public = public
        super().__init__(*args, **kwargs)

    def button_check(self, button: miru.Button, ctx: miru.Context) -> None:
        if (self.public or ctx.author.id == self.author.id) and button.label is not None:
            self.answer = button.label.lower()
            self.who_clicked = ctx.user
            self.stop()

    def cancel_button_check(self, button: miru.Button, ctx: miru.Context) -> None:
        if ctx.author.id == self.author.id and button.label is not None:
            self.answer = button.label.lower()
            self.stop()

    @miru.button(label="A", style=hikari.ButtonStyle.PRIMARY)
    async def a_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(label="B", style=hikari.ButtonStyle.PRIMARY)
    async def b_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(label="C", style=hikari.ButtonStyle.PRIMARY)
    async def c_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(label="D", style=hikari.ButtonStyle.PRIMARY)
    async def d_button(self, button: miru.Button, ctx: miru.Context) -> None:
        self.button_check(button, ctx)

    @miru.button(
        label="Cancel", emoji="\N{BLACK SQUARE FOR STOP}", style=hikari.ButtonStyle.DANGER, row=2
    )
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.cancel_button_check(button, ctx)


async def rps_player_vs_bot(ctx: lightbulb.Context) -> None:
    while True:
        view = RPSView(ctx.author, timeout=60)
        message = await ctx.respond(
            f"{ctx.author.mention} Pick a move!", components=view, user_mentions=True
        )
        await view.start(message)
        await view.wait()
        if hasattr(view, "move") and view.move != "cancel":
            game_string = f"{ctx.author.mention} Rock, paper, scissors, shoot!"
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

            # Get the moves that the bot would win / lose against
            bot_wins = RPS_WINLOSS[bot_move][0]
            bot_loses = RPS_WINLOSS[bot_move][1]

            if player_move == bot_wins:
                game_string += "\n\n**I win!**"
            elif player_move == bot_loses:
                game_string += "\n\n**You win.**"
            else:
                game_string += "\n\n**It's a draw.**"

            if not ctx.options.continue_after_draw or not game_string.endswith("draw.**"):
                await game.edit(game_string)
                break

            game_string += " Running it back."
            await game.edit(game_string)
            await asyncio.sleep(1)
        else:
            if hasattr(view, "move"):
                await ctx.respond("Cancelled.")
            else:
                await ctx.respond("You took too long. Cancelling.")
            break


async def rps_player_vs_player_accept(ctx: lightbulb.Context) -> None:
    opponent = ctx.options.opponent
    accept_view = RPSAcceptView(opponent, timeout=60)

    continue_after_draw_string = ""
    if not ctx.options.continue_after_draw:
        continue_after_draw_string = " (continue after draw turned off)"

    message = await ctx.respond(
        (
            f"{opponent.mention}\n\n{ctx.author.mention} has challenged you to"
            f" Rock-Paper-Scissors{continue_after_draw_string}!"
            " Do you accept? You have 60 seconds before the request times out."
        ),
        components=accept_view,
        user_mentions=True,
    )
    await accept_view.start(message)
    await accept_view.wait()
    if hasattr(accept_view, "option"):
        if accept_view.option == "accept":
            await rps_player_vs_player(ctx, opponent)
        else:
            await ctx.respond(f"{opponent.mention} has declined the match.")
    else:
        await ctx.respond(f"{opponent.mention} took too long to answer.")


async def rps_player_vs_player(ctx: lightbulb.Context, opponent: hikari.User) -> None:
    while True:
        # Player one (author) picks a move
        player_one_view = RPSView(ctx.author, timeout=60)
        player_one_message = await ctx.respond(
            f"{ctx.author.mention} Pick a move!",
            components=player_one_view,
            user_mentions=True,
        )
        await player_one_view.start(player_one_message)
        await player_one_view.wait()
        if not hasattr(player_one_view, "move") or player_one_view.move == "cancel":
            if hasattr(player_one_view, "move"):
                await ctx.respond(f"{ctx.author.mention} ditched the match.")
            else:
                await ctx.respond(f"{ctx.author.mention} took too long.")
            break

        # Player two (opponent) picks a move
        player_two_view = RPSView(opponent, timeout=60)
        player_two_message = await ctx.respond(
            f"{opponent.mention} Pick a move!",
            components=player_two_view,
            user_mentions=True,
        )
        await player_two_view.start(player_two_message)
        await player_two_view.wait()
        if not hasattr(player_two_view, "move") or player_two_view.move == "cancel":
            if hasattr(player_two_view, "move"):
                await ctx.respond(f"{opponent.mention} ditched the match.")
            else:
                await ctx.respond(f"{opponent.mention} took too long.")
            break

        game_string = f"{ctx.author.mention} {opponent.mention}\nRock, paper, scissors, shoot!"
        game = await ctx.respond(game_string, user_mentions=True)
        await asyncio.sleep(2)

        player_one_move = player_one_view.move
        player_two_move = player_two_view.move

        # Add both player moves at the same time instead of waiting per player
        game_string += (
            f"\n\n{RPS_EMOTES[player_one_move]} {ctx.author.mention} chose"
            f" {player_one_move}."
            f"\n{RPS_EMOTES[player_two_move]} {opponent.mention} chose"
            f" {player_two_move}."
        )
        await game.edit(game_string)
        await asyncio.sleep(1)

        # Decide the outcome
        player_two_wins = RPS_WINLOSS[player_two_move][0]
        player_two_loses = RPS_WINLOSS[player_two_move][1]

        if player_one_move == player_two_wins:
            game_string += f"\n\n**{opponent.mention} wins!**"
        elif player_one_move == player_two_loses:
            game_string += f"\n\n**{ctx.author.mention} wins!**"
        else:
            game_string += "\n\n**It's a draw.**"

        if not ctx.options.continue_after_draw or not game_string.endswith("draw.**"):
            await game.edit(game_string)
            break

        game_string += " Running it back."
        await game.edit(game_string)
        await asyncio.sleep(1)


@plugin.command
@lightbulb.option(
    name="opponent",
    description="Who to play against (default: play against me!)",
    type=hikari.User,
    default=None,
)
@lightbulb.option(
    name="continue_after_draw",
    description="Automatically start another match after a draw? (default: true)",
    type=bool,
    default=True,
)
@lightbulb.command(name="rps", description="Play Rock-Paper-Scissors")
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context) -> None:
    opponent = ctx.options.opponent
    if opponent is None or (
        (bot_user := ctx.bot.get_me()) is not None and opponent.id == bot_user.id
    ):
        await rps_player_vs_bot(ctx)
    elif opponent.id == ctx.author.id:
        await ctx.respond("You can't play against yourself!")
    else:
        await rps_player_vs_player_accept(ctx)


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
    if ctx.options.public:
        trivia_string[0] += "\n(Anyone can answer this!)"

    view = TriviaView(ctx.author, ctx.options.public, timeout=60)
    message = await ctx.respond("\n\n".join(trivia_string), components=view)
    await view.start(message)
    await view.wait()

    if hasattr(view, "answer"):
        if view.answer != "cancel":
            # Indicate the right answer with a check mark
            answers_list[answers.index(correct_answer)] += " :white_check_mark:"

            if answers_with_letters[view.answer] == correct_answer:
                await ctx.respond(
                    f"{view.who_clicked.mention} That is correct!", user_mentions=True
                )
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
            if ctx.options.public:
                trivia_string[0] += "\n(Anyone can answer this!)"
            await message.edit("\n\n".join(trivia_string))
        else:
            await ctx.respond("Cancelled.")
    else:
        await ctx.respond("You took too long to answer. Cancelling.")


@plugin.command
@lightbulb.option(
    name="max_number",
    description="I'll only think of a number from 1 to (max). (default: 100)",
    type=int,
    default=100,
    min_value=2,
    max_value=1_000_000,
)
@lightbulb.option(
    name="public",
    description="Can anyone try to guess the number? (default: False, only you can guess)",
    type=bool,
    default=False,
)
@lightbulb.command(name="guessinggame", description="Try to guess what number I'm thinking of")
@lightbulb.implements(lightbulb.SlashCommand)
async def guessinggame(ctx: lightbulb.Context) -> None:
    max_ = ctx.options.max_number
    number = random.randint(1, max_)
    guesses = 0

    await ctx.respond(
        f"{ctx.author.mention} I'm thinking of a number between 1 and {max_}...try to guess what"
        ' it is! (Type "cancel" to cancel.)'
    )

    while True:
        response = await ctx.bot.wait_for(
            hikari.GuildMessageCreateEvent,
            timeout=60,
            predicate=lambda e: ctx.options.public or e.message.author.id == ctx.author.id,
        )
        message = response.message
        guess = message.content

        if guess is not None and guess.isdigit():
            guesses += 1
            num = int(guess)
            if num < 1 or num > max_:
                await response.message.respond(
                    f"{message.author.mention} Your guess isn't between 1 and {max_}...try again!",
                    user_mentions=True,
                )
            elif num > number:
                await response.message.respond(
                    f"{message.author.mention} My number is lower. Try again!",
                    user_mentions=True,
                )
            elif num < number:
                await response.message.respond(
                    f"{message.author.mention} My number is higher. Try again!",
                    user_mentions=True,
                )
            else:
                await response.message.respond(
                    f"{message.author.mention} You got it! It took you {guesses} tries!",
                    user_mentions=True,
                )
                break
        elif guess is not None and guess.lower() == "cancel":
            await response.message.respond("Cancelled.")
            break


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
