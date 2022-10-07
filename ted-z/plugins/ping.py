import crescent

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="ping", description="Ping Ted")
async def ping(ctx: crescent.Context) -> None:
    await ctx.respond(f":ping_pong: Pong! ({round(ctx.app.heartbeat_latency * 1000)} ms)")
