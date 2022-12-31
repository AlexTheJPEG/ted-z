import random

import asyncio
import crescent
import hikari
import miru


plugin = crescent.Plugin()

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
        await ctx.respond("Cancelled.", flags=hikari.MessageFlag.EPHEMERAL)
        self.stop()


@plugin.include
@crescent.command(name="rps", description="Play rock-paper-scissors")
class RPSCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        view = RPSView(timeout=60)
        message = await ctx.respond(
            "Pick a move!", components=view, ephemeral=True, ensure_message=True
        )
        await view.start(message)
        await view.wait()
        if hasattr(view, "move"):
            game_string = f"{ctx.user.mention}\nRock, paper, scissors, shoot!"
            game = await ctx.respond(game_string, ensure_message=True, user_mentions=True)
            await asyncio.sleep(2)

            player_move = view.move
            bot_move = random.choice(list(RPS_EMOTES.keys()))

            game_string += f"\n\n{RPS_EMOTES[player_move]} You chose {player_move}."
            await game.edit(game_string)
            await asyncio.sleep(1)

            game_string += f"\n{RPS_EMOTES[bot_move]} I chose {bot_move}."
            await game.edit(game_string)
            await asyncio.sleep(1)

            self.bot_wins = RPS_WINLOSS[bot_move][0]
            self.bot_loses = RPS_WINLOSS[bot_move][1]

            match player_move:
                case self.bot_wins:
                    game_string += f"\n\n**I win!**"
                case self.bot_loses:
                    game_string += f"\n\n**You win.**"
                case _:
                    game_string += f"\n\n**It's a draw.**"
            await game.edit(game_string)
