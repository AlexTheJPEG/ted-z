from io import BytesIO
import os
import random
import tempfile

import aiohttp
from gazpacho.soup import Soup
import hikari
import lightbulb
import PIL
from PIL import Image, ImageOps

from ..utils.web import HEADERS

plugin = lightbulb.Plugin("images")


@plugin.command
@lightbulb.option(name="user", description="The user to get the avatar from", type=hikari.User)
@lightbulb.command(name="avatar", description="Get the user's avatar as an image")
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar(ctx: lightbulb.Context) -> None:
    await ctx.respond(
        f"{ctx.options.user.mention}'s avatar:", attachment=ctx.options.user.avatar_url
    )


@plugin.command
@lightbulb.option(name="image", description="The image to JPEGify", type=hikari.Attachment)
@lightbulb.command(name="jpegify", description="Add some JPEG crustiness to an image")
@lightbulb.implements(lightbulb.SlashCommand)
async def jpegify(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(ctx.options.image.url) as response:
            image = Image.open(BytesIO(await response.read()))

    try:
        image = image.convert("RGB")

        with tempfile.NamedTemporaryFile(suffix=".jpg") as file:
            image.save(file, format="JPEG", optimize=True, quality=0)
            await ctx.respond(attachment=file.name)
    except PIL.UnidentifiedImageError:
        await ctx.respond("Looks like you didn't send an image! Come back with one and try again.")


@plugin.command
@lightbulb.option(name="image", description="The image to invert", type=hikari.Attachment)
@lightbulb.command(name="invert", description="Invert an image's colors")
@lightbulb.implements(lightbulb.SlashCommand)
async def invert(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(ctx.options.image.url) as response:
            image = Image.open(BytesIO(await response.read()))
    _, extension = os.path.splitext(ctx.options.image.url)

    try:
        if extension == ".png":
            image = image.convert("RGBA")

            with tempfile.NamedTemporaryFile(suffix=extension) as file:
                r, g, b, a = image.split()

                r = r.point(lambda i: 255 - i)
                g = g.point(lambda i: 255 - i)
                b = b.point(lambda i: 255 - i)

                inverted_image = Image.merge("RGBA", (r, g, b, a))
                inverted_image.save(file)
                await ctx.respond(attachment=file.name)
        else:
            image = image.convert("RGB")

            with tempfile.NamedTemporaryFile(suffix=extension) as file:
                inverted_image = ImageOps.invert(image)
                inverted_image.save(file)
                await ctx.respond(attachment=file.name)
    except PIL.UnidentifiedImageError:
        await ctx.respond("Looks like you didn't send an image! Come back with one and try again.")


@plugin.command
@lightbulb.command(name="wikihow", description="Get a random Wikihow image")
@lightbulb.implements(lightbulb.SlashCommand)
async def wikihow(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://wikihow.com/Special:Randomizer", headers=HEADERS
        ) as response:
            article = Soup(await response.text())

    images = article.find("li", {"id": "step-id"})

    await ctx.respond(attachment=random.choice(images).find("img")[1].attrs["src"])  # type: ignore


async def color():
    pass


async def gradient():
    pass


async def apod():
    # https://api.nasa.gov/
    pass


async def yugioh():
    # https://ygoprodeck.com/api-guide/
    pass


async def xkcd():
    # https://xkcd.com/
    pass


async def person():
    # https://thispersondoesnotexist.com/
    pass


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
