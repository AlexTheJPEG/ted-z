import os
import random
import re
from io import BytesIO

import aiohttp
import hikari
import lightbulb
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

from ..utils.opening import load_bot_settings
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
    attachment = ctx.options.image
    media = attachment.media_type

    if media.startswith("image"):
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                image = Image.open(BytesIO(await response.read()))

        image = image.convert("RGB")

        buffer = BytesIO()
        image.save(buffer, format="JPEG", optimize=True, quality=0)

        filename, _ = os.path.splitext(attachment.filename)
        await ctx.respond(attachment=hikari.Bytes(buffer.getvalue(), f"{filename}-jpegify.jpg"))
    else:
        await ctx.respond("Looks like you didn't send an image! Come back with one and try again.")


@plugin.command
@lightbulb.option(name="image", description="The image to invert", type=hikari.Attachment)
@lightbulb.command(name="invert", description="Invert an image's colors")
@lightbulb.implements(lightbulb.SlashCommand)
async def invert(ctx: lightbulb.Context) -> None:
    attachment = ctx.options.image
    media = attachment.media_type

    if media.startswith("image"):
        async with aiohttp.ClientSession() as session:
            async with session.get(ctx.options.image.url) as response:
                image = Image.open(BytesIO(await response.read()))

        format = image.format

        if image.mode == "RGBA":
            # Map each RGB channel to its inverse, leave alpha alone
            image = image.convert("RGBA")

            r, g, b, a = image.split()

            r = r.point(lambda i: 255 - i)
            g = g.point(lambda i: 255 - i)
            b = b.point(lambda i: 255 - i)

            inverted_image = Image.merge("RGBA", (r, g, b, a))
        else:
            # Use the ImageOps method, which takes less lines
            image = image.convert("RGB")
            inverted_image = ImageOps.invert(image)

        buffer = BytesIO()
        inverted_image.save(buffer, format=format)

        filename, extension = os.path.splitext(attachment.filename)
        await ctx.respond(
            attachment=hikari.Bytes(buffer.getvalue(), f"{filename}-inverted.{extension}")
        )
    else:
        await ctx.respond("Looks like you didn't send an image! Come back with one and try again.")


@plugin.command
@lightbulb.command(name="wikihow", description="Get a random Wikihow image")
@lightbulb.implements(lightbulb.SlashCommand)
async def wikihow(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://wikihow.com/Special:Randomizer", headers=HEADERS
        ) as response:
            article = BeautifulSoup(await response.text(), "html.parser")

    steps = article.find_all("li", id=re.compile(r"step-id-\d+"))

    image = random.choice(steps).find("img")["data-srclarge"]

    await ctx.respond(attachment=f"https://www.wikihow.com{image}")


@plugin.command
@lightbulb.command(name="color", description="Generate a random color")
@lightbulb.implements(lightbulb.SlashCommand)
async def color(ctx: lightbulb.Context) -> None:
    hex_chars = "0123456789ABCDEF"
    random_hex = "".join([random.choice(hex_chars) for _ in range(6)])

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://www.thecolorapi.com/id?hex={random_hex}", headers=HEADERS
        ) as response:
            color_json = await response.json()

    rgb = color_json["rgb"]["value"]
    hsl = color_json["hsl"]["value"]
    hsv = color_json["hsv"]["value"]
    cmyk = color_json["cmyk"]["value"]

    name = color_json["name"]["value"]
    closest = color_json["name"]["closest_named_hex"]
    exact = color_json["name"]["exact_match_name"]

    r, g, b = color_json["rgb"]["r"], color_json["rgb"]["g"], color_json["rgb"]["b"]
    image = Image.new("RGB", (300, 300), (r, g, b))

    color_string = f"**#{random_hex}**\n{rgb}\n{hsl}\n{hsv}\n{cmyk}\n\n"
    if exact:
        color_string += f"Name: **{name}**"
    else:
        color_string += f"Closest named color: **{name}** ({closest})"

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    await ctx.respond(
        color_string, attachment=hikari.Bytes(buffer.getvalue(), f"{random_hex}.png")
    )


@plugin.command
@lightbulb.command(name="apod", description="Get NASA's Astronomy Picture of the Day")
@lightbulb.implements(lightbulb.SlashCommand)
async def apod(ctx: lightbulb.Context):
    try:
        nasa_api = load_bot_settings()["api"]["nasa"]
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.nasa.gov/planetary/apod?api_key={nasa_api}", headers=HEADERS
            ) as response:
                apod_json = await response.json()

        title = apod_json["title"]
        explanation = apod_json["explanation"]
        image = apod_json["url"]

        await ctx.respond(f"**{title}**\n\n{explanation}", attachment=image)
    except KeyError:
        await ctx.respond(
            "Seems you don't have a NASA API key! Try putting one in your bot settings file to use"
            " this command."
        )


@plugin.command
@lightbulb.command(name="yugioh", description="Get a random Yu-Gi-Oh! card")
@lightbulb.implements(lightbulb.SlashCommand)
async def yugioh(ctx: lightbulb.Context):
    # https://ygoprodeck.com/api-guide/
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://db.ygoprodeck.com/api/v7/randomcard.php", headers=HEADERS
        ) as response:
            yugioh_json = await response.json()

    card_image = yugioh_json["card_images"][0]

    await ctx.respond(attachment=card_image["image_url"])


@plugin.command
@lightbulb.command(name="xkcd", description="Get a random XKCD comic")
@lightbulb.implements(lightbulb.SlashCommand)
async def xkcd(ctx: lightbulb.Context):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://c.xkcd.com/random/comic/", headers=HEADERS) as response:
            website = BeautifulSoup(await response.text(), "html.parser")

    image = website.select("#comic > img")[0]
    image_url = image["src"]

    # Not confusing at all
    image_alt = image["title"]
    comic_title = image["alt"]

    link = website.select("#middleContainer > a:nth-child(6)")[0]["href"]

    await ctx.respond(
        f"**{comic_title}**\n{link}\n\n__Alt text__\n{image_alt}",
        attachment=f"https:{image_url}",
        flags=hikari.MessageFlag.SUPPRESS_EMBEDS,
    )


@plugin.command
@lightbulb.command(name="person", description="Generate a random person that does not exist")
@lightbulb.implements(lightbulb.SlashCommand)
async def person(ctx: lightbulb.Context):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://thispersondoesnotexist.com/image", headers=HEADERS
        ) as response:
            image = Image.open(BytesIO(await response.read()))

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    await ctx.respond(attachment=hikari.Bytes(buffer.getvalue(), f"person.png"))


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
