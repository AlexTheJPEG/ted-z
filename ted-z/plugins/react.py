import lightbulb

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

plugin = lightbulb.Plugin("react")


@plugin.command
@lightbulb.option(name="question", description="The question for the poll", type=str)
@lightbulb.command(name="yesno", description="Create a yes/no poll")
@lightbulb.implements(lightbulb.SlashCommand)
async def yesno(ctx: lightbulb.Context) -> None:
    msg = await (
        await ctx.respond(
            f"{ctx.options.question}\n\n(React :thumbsup: for yes and :thumbsdown: for no)",
        )
    ).message()
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@plugin.command
@lightbulb.option(name="question", description="The question for the poll", type=str)
@lightbulb.command(name="scale", description="Create a scale from 1-10 poll")
@lightbulb.implements(lightbulb.SlashCommand)
async def scale(ctx: lightbulb.Context) -> None:
    msg = await (
        await ctx.respond(f"{ctx.options.question}\n\n(React on a scale from 1 to 10)")
    ).message()
    for number in NUMBER_EMOTES:
        await msg.add_reaction(number)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)
