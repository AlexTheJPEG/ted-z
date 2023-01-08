from ..utils.opening import load_json

from libretranslatepy import LibreTranslateAPI
import lightbulb

LT_API = LibreTranslateAPI("https://lt.vern.cc/")
LANGUAGE_LIST = LT_API.languages()
LANGUAGE_DICT = {language["code"]: language["name"] for language in LANGUAGE_LIST}
LANGUAGE_DICT_REV = {language["name"]: language["code"] for language in LANGUAGE_LIST}

LANGUAGE_CODES = list(LANGUAGE_DICT.keys())
LANGUAGES = LANGUAGE_CODES + list(LANGUAGE_DICT_REV.keys())
LANGUAGE_CHOICES = [f"{k}: {v}\n" for k, v in LANGUAGE_DICT]

plugin = lightbulb.Plugin("translate")


@plugin.command
@lightbulb.command(
    name="langcodes",
    description="Display the possible languages you can use and their codes",
    ephemeral=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def langcodes(ctx: lightbulb.Context) -> None:
    # TODO: Make this a paginated embed
    await ctx.respond(
        "Here is a list of every language you can use with translate commands, "
        "as well as the language codes they correspond to. You can use either the full "
        "language name or the two-letter code.\n\n"
        f"{''.join(LANGUAGE_CHOICES)}"
    )


@plugin.command
@lightbulb.option(name="phrase", description="The phrase to translate", type=str)
@lightbulb.option(name="destination", description="The language to translate to", type=str)
@lightbulb.option(name="source", description="The source language", type=str)
@lightbulb.command(name="translate", description="Translate a phrase from one language to another")
@lightbulb.implements(lightbulb.SlashCommand)
async def translate(ctx: lightbulb.Context) -> None:
    if ctx.options.source == "detect":
        # TODO: Add language detection; this library doesn't seem to have it
        await ctx.respond("Sorry, language detection isn't a thing yet; try again later!")
    else:
        match (ctx.options.source.lower(), ctx.options.destination.lower()):
            case (src, dest) if src in LANGUAGES and dest in LANGUAGES:
                if len(src) != 2:
                    src = LANGUAGE_DICT_REV[src.lower()]
                if len(dest) != 2:
                    dest = LANGUAGE_DICT_REV[dest.lower()]
                translation = LT_API.translate(ctx.options.phrase, src, dest)
                await ctx.respond(
                    f":speech_balloon: **{ctx.options.phrase}**"
                    f" translated from {LANGUAGE_DICT[src].title()} to {LANGUAGE_DICT[dest].title()}:"
                    f"\n\n{translation}"
                )
            case (src, _) if src not in LANGUAGES:
                await ctx.respond(
                    f"The source ({src}) language is either invalid or unsupported!"
                    "\n\nUse `/langcodes` to see what languages you can use."
                )
            case (_, dest) if dest not in LANGUAGES:
                await ctx.respond(
                    f"The destination ({dest}) language is either invalid or unsupported!"
                    "\n\nUse `/langcodes` to see what languages you can use."
                )


# TODO: Bad translate command


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
