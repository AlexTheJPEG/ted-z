<p align="center">
    <img width="200" src="./assets/ted.svg" alt="Ted face">
</p>

# Ted Z
~~this is the last revision i swear~~

Just another Discord bot written in Python that does anything a Discord bot usually does!
Written using [Hikari](https://github.com/hikari-py/hikari) and [Lightbulb](https://github.com/tandemdude/hikari-lightbulb).

## Setup
To get started, [create a Discord application](https://discord.com/developers/applications) and add a bot user for it. Then scroll down and make sure the **"Message content intent"** option is toggled on.

After you've made your application, clone this repo somewhere on your machine, then create a file in the project directory called `bot_settings.toml`. This will contain all the settings required for the bot.

The file should contain at least the following settings:
```toml
[bot]
token = "[bot token]"
```

Other settings include:
```toml
[api]
nasa = "[nasa api token]"  # needed for /apod
```

As for dependencies, they are all handled by [Poetry](https://github.com/python-poetry/poetry). Install Poetry on your machine if you haven't already, then simply run `poetry install` in the project directory.

To run the bot, activate the virtual environment created by Poetry using `poetry shell` and run `python -m ted-z` in the project directory.

## Notes
An alternative way to run your bot without explicitly activating the virtual environment is by running `poetry run python -m ted-z`. If you're running the bot on VSCode or a Python IDE, the virtual environment may be activated automatically.

If your bot is online, and you change its code in one of the plugins, you may use `/reload [plugin]` in a valid text channel to reload the plugin (or use `/reload all` or simply `/reload` to reload all plugins) without having to restart the entire bot. Creating or deleting plugins / commands still requires a full restart.
