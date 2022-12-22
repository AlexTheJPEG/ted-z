import os
import json
import random

import crescent

from goslate import Goslate

TRANSLATOR = Goslate()
LANGUAGES = TRANSLATOR.get_languages()
LANGUAGE_CODES = list(LANGUAGES.keys())
LANGUAGE_CHOICES = [f"{k}: {v.title()}\n" for k, v in LANGUAGES.items()]

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="langcodes", description="Display the possible languages you can use and their codes")
class LangCodesCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        # TODO: Make this a paginated embed
        await ctx.respond("Here is a list of every language code you can use with translate commands,"
                        "as well as the languages they correspond to:\n\n"
                        f"{''.join(LANGUAGE_CHOICES)}", ephemeral=True)


@plugin.include
@crescent.command(name="translate", description="Translate a phrase from one language to another")
class TranslateCommand:
    source = crescent.option(str, "The source language (use \"detect\" to autodetect the language)")
    destination = crescent.option(str, "The language to translate to")
    phrase = crescent.option(str, "The phrase to translate")

    async def callback(self, ctx: crescent.Context) -> None:
        match (self.source, self.destination):
            case ("detect", dest) if dest in LANGUAGE_CODES:
                await ctx.respond(f"💬 **{self.phrase}** translated to {LANGUAGES[dest].title()}:"
                                f"\n\n{TRANSLATOR.translate(text=self.phrase, target_language=dest)}")
            case (src, dest) if src in LANGUAGE_CODES and dest in LANGUAGE_CODES:
                await ctx.respond(f"💬 **{self.phrase}** translated from {LANGUAGES[src].title()} to {LANGUAGES[dest].title()}:"
                                f"\n\n{TRANSLATOR.translate(text=self.phrase, target_language=dest, source_language=src)}")
            case _:
                await ctx.respond(f"Either the source ({self.source}) or the destination ({self.destination}) language (or both) is invalid!"
                                  "\n\nUse `/langcodes` to see what languages you can use. "
                                  "You can also use \"detect\" as the source language to autodetect the language.")


# TODO: Bad translate command
