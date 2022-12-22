import os
import json
import random
from typing import Annotated as Atd

import crescent

from translate import Translator

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
with open(f"{dir_path}/files/langcodes.json", 'r') as file:
    LANGUAGES = json.load(file)

LANGUAGE_CODES = list(LANGUAGES.keys())
LANGUAGE_CHOICES = [f"{k}: {v.title()}\n" for k, v in LANGUAGES.items()]

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="langcodes", description="Display the possible languages you can use and their codes")
async def langcodes(ctx: crescent.Context) -> None:
    # TODO: Make this a paginated embed
    await ctx.respond("Here is a list of every language code you can use with translate commands,"
                      "as well as the languages they correspond to:\n\n"
                      f"{''.join(LANGUAGE_CHOICES)}", ephemeral=True)


@plugin.include
@crescent.command(name="translate", description="Translate a phrase from one language to another")
async def translate(ctx: crescent.Context,
                    destination: Atd[str, "The language to translate to"],
                    phrase: Atd[str, "The phrase to translate"],
                    source: Atd[str, "The source language (auto-detects by default)"] | None = None,
                    ) -> None:
    match [source, destination]:
        case [None, dest] if dest.lower() in LANGUAGE_CODES:
            translator = Translator(to_lang=dest)
            translation = translator.translate(phrase)
            await ctx.respond(f"💬 **{phrase}** translated to {LANGUAGES[dest].title()}:"
                              f"\n\n{translation}")
        case [src, dest] if src.lower() in LANGUAGE_CODES and dest.lower() in LANGUAGE_CODES:
            translator = Translator(from_lang=src, to_lang=dest)
            translation = translator.translate(phrase)
            await ctx.respond(f"💬 **{phrase}** translated from {LANGUAGES[src].title()} to {LANGUAGES[dest].title()}:"
                              f"\n\n{translation}")
        case _:
            await ctx.respond("❗ The source and/or desination language is invalid!"
                              "Use `/langcodes` to see what languages you can use.", ephemeral=True)


# TODO: Bad translate command
