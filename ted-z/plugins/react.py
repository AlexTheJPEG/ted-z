import crescent

plugin = crescent.Plugin()

NUMBER_EMOTES = [
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟",
]


@plugin.include
@crescent.command(name="yesno", description="Create a yes/no poll")
class YesNoCommand:
    question = crescent.option(str, "The question for the poll")

    async def callback(self, ctx: crescent.Context) -> None:
        msg = await ctx.respond(
            f"{self.question}\n\n(React :thumbsup: for yes and :thumbsdown: for no)",
            ensure_message=True,
        )
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


@plugin.include
@crescent.command(name="scale", description="Create a scale from 1-10 poll")
class ScaleCommand:
    question = crescent.option(str, "The question for the poll")

    async def callback(self, ctx: crescent.Context) -> None:
        msg = await ctx.respond(
            f"{self.question}\n\n(React on a scale from 1 to 10)", ensure_message=True
        )
        for number in NUMBER_EMOTES:
            await msg.add_reaction(number)
