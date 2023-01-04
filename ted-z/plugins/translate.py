from ..utils.opening import load_json

import argostranslate.translate
import crescent

LANGUAGE_DICT = load_json("langcodes.json")
LANGUAGE_DICT_REV = {value: key for key, value in LANGUAGE_DICT.items()}

LANGUAGE_CODES = list(LANGUAGE_DICT.keys())
LANGUAGES = LANGUAGE_CODES + list(LANGUAGE_DICT.values())
LANGUAGE_CHOICES = [f"{key}: {value.title()}\n" for key, value in LANGUAGE_DICT.items()]

# Uncomment these lines to install all the translation language models
# import argostranslate.package
# argostranslate.package.update_package_index()
# available_packages = argostranslate.package.get_available_packages()
# for package in available_packages:
#     argostranslate.package.install_from_path(package.download())

plugin = crescent.Plugin()


@plugin.include
@crescent.command(
    name="langcodes",
    description="Display the possible languages you can use and their codes",
)
class LangCodesCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        # TODO: Make this a paginated embed
        await ctx.respond(
            "Here is a list of every language you can use with translate commands, "
            "as well as the language codes they correspond to. You can use either the full "
            "language name or the two-letter code.\n\n"
            f"{''.join(LANGUAGE_CHOICES)}",
            ephemeral=True,
        )


@plugin.include
@crescent.command(name="translate", description="Translate a phrase from one language to another")
class TranslateCommand:
    source = crescent.option(
        str, "The source language"
    )  # (use \"detect\" to autodetect the language)")
    destination = crescent.option(str, "The language to translate to")
    phrase = crescent.option(str, "The phrase to translate")

    async def callback(self, ctx: crescent.Context) -> None:
        if self.source == "detect":
            # TODO: Add language detection; this library doesn't seem to have it
            await ctx.respond("Sorry, language detection isn't a thing yet; try again later!")
        else:
            match (self.source.lower(), self.destination.lower()):
                case (src, dest) if src in LANGUAGES and dest in LANGUAGES:
                    if len(src) != 2:
                        src = LANGUAGE_DICT_REV[src.lower()]
                    if len(dest) != 2:
                        dest = LANGUAGE_DICT_REV[dest.lower()]
                    translation = argostranslate.translate.translate(self.phrase, src, dest)
                    await ctx.respond(
                        f":speech_balloon: **{self.phrase}**"
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
