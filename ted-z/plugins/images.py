import hikari
import lightbulb

plugin = lightbulb.Plugin("images")


@plugin.command
@lightbulb.option(name="user", description="The user to get the avatar from", type=hikari.User)
@lightbulb.command(name="avatar", description="Get the user's avatar as an image")
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar(ctx: lightbulb.Context) -> None:
    await ctx.respond(
        f"{ctx.options.user.mention}'s avatar:", attachment=ctx.options.user.avatar_url
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
