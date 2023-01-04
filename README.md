# Ted Z
~~this is the last revision i swear~~

Just another Discord bot written in Python that does anything a Discord bot usually does!
Written using [Hikari](https://github.com/hikari-py/hikari) and [Crescent](https://github.com/magpie-dev/hikari-crescent).

## Setup
To get started, clone this repo somewhere on your machine, then create a file in the project directory called `bot_settings.toml`. This will contain all the settings required for the bot.

The file should contain at least the following settings:
```
[bot]
token = "[bot token]"
username = "[bot username]#[bot discriminator]"
```

As for dependencies, they are all handled by [Poetry](https://github.com/python-poetry/poetry). Simply run `poetry install` in the project directory.

To run the bot, activate the virtual environment created by Poetry and run `python -m ted-z` in the project directory.

## Notes
If your bot is online, and you change its code in one of the plugins, you may use `/reload [plugin]` in a valid text channel to reload the plugin (or use `/reload all` or simply `/reload` to reload all plugins) without having to restart the entire bot. Creating or deleting plugins still requires a full restart.