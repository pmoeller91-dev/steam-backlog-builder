import asyncio
from steamid.steamid import SteamID
from steamid.resolve_custom_id import InvalidCustomIDError
from steamlib.get_owned_games import get_owned_games, AuthFailedError
from os import environ
import argparse
import random
import sys

parser = argparse.ArgumentParser(
    description=(
        "Picks a random steam game from your backlog for you to play"
        " next! Any game with less than one hour of playtime is eligible"
        " to be picked."
    ),
)
parser.add_argument(
    "steam_id",
    help="The Steam ID to pick a backlog game for.",
    metavar="SteamID",
)
parser.add_argument(
    "--steam-api-key",
    "-s",
    help=(
        "The Steam API key to use to retrieve owned games with. If not provided,"
        " it will be read from the STEAM_API_KEY environment variable."
        " If it cannot be found in either location, the program will not run."
    ),
    metavar="api_key",
    dest="steam_api_key",
)


def get_duration_str(mins: int) -> str:
    """Provide a remark depending on a given game's playtime.

    Args:
        mins (int): Number of minutes previously played.

    Returns:
        str: A relevant remark for the number of minutes.
    """
    if mins == 0:
        return "You haven't played it at all yet!"
    return f"You've only played it for {mins} minute{'' if mins == 1 else 's'} so far!"


async def main():
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    id: str = args.steam_id
    api_key = args.steam_api_key or environ.get("STEAM_API_KEY")
    if not isinstance(api_key, str) or len(api_key) == 0:
        print(
            "You must provide a Steam Web API key to use this program. To"
            " generate one for your account, please visit the following"
            " link: https://steamcommunity.com/dev/apikey. Anything can be"
            " provided for the domain, but if you are using it only for this"
            " application, 'localhost' is a good bet."
            "\n"
            "\n"
            "Once you have an API key, it can be provided using the"
            " --steam-api-key argument, or by setting the environment variable"
            " STEAM_API_KEY to the correct value."
            "\n"
            "\n"
            "Warning: A Steam API key is *sensitive*! Do not share it with"
            " anyone, nor use it with any program you do not trust. Once"
            " you are done using your API key, try to remember to revoke it"
            " by using the same link."
        )
        sys.exit(1)

    try:
        steam_id = SteamID(id)
        id_64 = await steam_id.to_steam_id_64()
    except ValueError:
        print(f'Could not parse the provided Steam ID: "{id}"')
        sys.exit(3)
    except InvalidCustomIDError:
        print(f'Could not find a Steam profile associated with the Custom ID: "{id}"')
        sys.exit(3)

    try:
        owned_games = await get_owned_games(id_64, api_key)
    except AuthFailedError as e:
        print(
            "Could not retrieve the Steam games owned by that Steam ID!"
            "\n\nIt's possible the API key provided is invalid, or the Steam ID"
            " specified does not have a public profile, or a profile accessible"
            " by the account associated with the API key."
            "\n\nPlease double check"
            " the API key and the Steam profile in question and try again."
        )
        sys.exit(2)

    short_play_games = [game for game in owned_games if game["playtime_forever"] < 60]
    if len(short_play_games) == 0:
        print(
            "Wow! You don't have any unplayed games. "
            "Either you haven't gotten started yet, or you've "
            "done a great job cleaning up your backlog! "
            "Get out there and buy something new."
        )
        sys.exit(0)

    random_game = random.choice(short_play_games)
    print(
        f"Why not try playing {random_game['name']}? {get_duration_str(random_game['playtime_forever'])}"
    )


asyncio.run(main())
