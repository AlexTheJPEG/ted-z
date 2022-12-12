from typing import Annotated as Atd

import crescent

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="yesno", description="Create a yes/no poll")
async def yesno(ctx: crescent.Context, question: Atd[str, "The question for the poll"]) -> None:
    msg = await ctx.respond(f"{question}\n\n(React :thumbsup: for yes and :thumbsdown: for no)", ensure_message=True)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@plugin.include
@crescent.command(name="scale", description="Create a scale from 1-10 poll")
async def scale(ctx: crescent.Context, question: Atd[str, "The question for the poll"]) -> None:
    number_emotes = [
        '1️⃣',
        '2️⃣',
        '3️⃣',
        '4️⃣',
        '5️⃣',
        '6️⃣',
        '7️⃣',
        '8️⃣',
        '9️⃣',
        '🔟',
    ]
    msg = await ctx.respond(f"{question}\n\n(React on a scale from 1 to 10)", ensure_message=True)
    for number in number_emotes:
        await msg.add_reaction(number)