import lightbulb

plugin = lightbulb.Plugin("admin")


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option(
    name="plugin",
    description="The plugin to reload (default: all)",
    choices=(
        "all",
        "ping",
        "rand",
        "react",
        "fun",
        "translate",
        "admin",
    ),
    default="all",
)
@lightbulb.command(name="reload", description="Reloads a plugin, or all of them", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context) -> None:
    if ctx.options.plugin == "all":
        ctx.bot.reload_extensions(*ctx.bot.extensions)
    else:
        ctx.bot.reload_extensions(f"ted-z.plugins.{ctx.options.plugin}")

    await ctx.bot.sync_application_commands()

    if ctx.options.plugin == "all":
        await ctx.respond("All plugins reloaded!")
    else:
        await ctx.respond(f"`{ctx.options.plugin}` plugin reloaded!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
