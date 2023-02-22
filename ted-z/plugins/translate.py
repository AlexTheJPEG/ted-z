import random

import lightbulb
from libretranslatepy import LibreTranslateAPI

LT_API = LibreTranslateAPI("https://translate.terraprint.co/")
LANGUAGE_LIST = LT_API.languages()
LANGUAGE_DICT = {language["code"]: language["name"].lower() for language in LANGUAGE_LIST}
LANGUAGE_DICT_REV = {language["name"].lower(): language["code"] for language in LANGUAGE_LIST}

LANGUAGE_CODES = list(LANGUAGE_DICT.keys())
LANGUAGES = LANGUAGE_CODES + list(LANGUAGE_DICT_REV.keys())
LANGUAGE_CHOICES = [f"{k}: {v.title()}\n" for k, v in LANGUAGE_DICT]

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
        "Here is a list of every language you can use with translate commands, as well as the"
        " language codes they correspond to. You can use either the full language name or the"
        f" two-letter code.\n\n{''.join(LANGUAGE_CHOICES)}"
    )


@plugin.command
@lightbulb.option(name="phrase", description="The phrase to translate", type=str)
@lightbulb.option(name="destination", description="The language to translate to", type=str)
@lightbulb.option(name="source", description="The source language", type=str)
@lightbulb.command(name="translate", description="Translate a phrase from one language to another")
@lightbulb.implements(lightbulb.SlashCommand)
async def translate(ctx: lightbulb.Context) -> None:
    source = ctx.options.source.lower()
    destination = ctx.options.destination.lower()

    if ctx.options.source == "detect":
        source = LT_API.detect(ctx.options.phrase)[0]["language"]

    match (source, destination):
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
                f':exclamation: The source language "{src}" is either invalid or unsupported!'
                "\n\nUse `/langcodes` to see what languages you can use."
            )
        case (_, dest) if dest not in LANGUAGES:
            await ctx.respond(
                f':exclamation: The destination language "{dest}" is either invalid or'
                " unsupported!\n\nUse `/langcodes` to see what languages you can use."
            )


@plugin.command
@lightbulb.option(name="phrase", description="The phrase to badly translate", type=str)
@lightbulb.option(
    name="iterations",
    description="The number of languages to go through",
    type=int,
    min_value=1,
    max_value=20,
)
@lightbulb.option(name="source", description="The source language", type=str)
@lightbulb.command(
    name="badtranslate",
    description="Go through a language translator multiple times to see how bad it gets",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def badtranslate(ctx: lightbulb.Context) -> None:
    source = ctx.options.source.lower()
    original_phrase = ctx.options.phrase

    if source == "detect":
        source = LT_API.detect(original_phrase)[0]["language"]
    if source not in LANGUAGES:
        await ctx.respond(
            f"The source ({source}) language is either invalid or unsupported!"
            "\n\nUse `/langcodes` to see what languages you can use."
        )
    else:
        if len(source) != 2:
            source = LANGUAGE_DICT_REV[source.lower()]

        badtranslate_string = (
            ":anger_right: Beginning your bad translation. It may take a while depending on how"
            " many languages you have to go through."
        )
        message = await ctx.respond(badtranslate_string)

        translated_phrase = ctx.options.phrase
        iterations = ctx.options.iterations
        used_languages = random.sample(LANGUAGE_CODES, iterations)

        current_src = source

        for index, language in enumerate(used_languages):
            translated_phrase = LT_API.translate(translated_phrase, current_src, language)

            current_src = language

            if (index + 1) % 2 == 0:
                ratio = (index + 1) / iterations
                percentage = int(ratio * 100)
                blocks = int(ratio * 10)

                progress_bar = ":green_square:" * blocks + ":white_large_square:" * (10 - blocks)

                await message.edit(f"{badtranslate_string}\n\n{progress_bar} ({percentage}%)")

        await message.edit(f"{badtranslate_string}\n\n{':green_square:' * 10} (100%)")

        translated_phrase = LT_API.translate(translated_phrase, current_src, source)

        language_chain = " -> ".join(used_languages)
        await ctx.respond(
            f"Translating **{original_phrase}** from {source} -> {language_chain} ->"
            f" {source} gives us:\n\n{translated_phrase}"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
