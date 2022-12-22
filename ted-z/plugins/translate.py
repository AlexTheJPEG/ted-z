import os
import json
import random

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
class LangCodesCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        # TODO: Make this a paginated embed
        await ctx.respond("Here is a list of every language code you can use with translate commands,"
                        "as well as the languages they correspond to:\n\n"
                        f"{''.join(LANGUAGE_CHOICES)}", ephemeral=True)


@plugin.include
@crescent.command(name="translate", description="Translate a phrase from one language to another")
class TranslateCommand:
    phrase = crescent.option(str, "The phrase to translate")
    destination = crescent.option(str, "The langauge to translate to")
    source = crescent.option(str, "The source language (auto-detects by default)", default=None)

    async def callback(self, ctx: crescent.Context) -> None:
        # FIXME: Doesn't translate for some reason
        match [self.source, self.destination]:
            case [None, dest] if dest.lower() in LANGUAGE_CODES:
                translator = Translator(to_lang=dest)
                translation = translator.translate(self.phrase)
                await ctx.respond(f"💬 **{self.phrase}** translated to {LANGUAGES[dest].title()}:"
                                f"\n\n{translation}")
            case [src, dest] if src.lower() in LANGUAGE_CODES and dest.lower() in LANGUAGE_CODES:
                translator = Translator(from_lang=src, to_lang=dest)
                translation = translator.translate(self.phrase)
                await ctx.respond(f"💬 **{self.phrase}** translated from {LANGUAGES[src].title()} to {LANGUAGES[dest].title()}:"
                                f"\n\n{translation}")
            case _:
                await ctx.respond("❗ The source and/or desination language is invalid!"
                                  "Use `/langcodes` to see what languages you can use.", ephemeral=True)


# TODO: Bad translate command
