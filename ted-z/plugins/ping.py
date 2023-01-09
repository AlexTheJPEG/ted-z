import lightbulb

plugin = lightbulb.Plugin("ping")


@plugin.command
@lightbulb.command(name="ping", description="Ping Ted")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f":ping_pong: Pong! ({round(ctx.app.heartbeat_latency * 1000)} ms)")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
