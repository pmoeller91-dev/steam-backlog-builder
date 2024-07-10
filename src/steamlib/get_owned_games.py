from typing import Any, TypedDict
import aiohttp
import json
from .error import AuthFailedError

class OwnedGame(TypedDict):
    name: str
    playtime_forever: int
    appid: int


async def get_owned_games(steam_id_64: str, steam_api_key: str) -> list[OwnedGame]:
    """Gets a list of games owned by an account. May fail if the account is
    private, or if the Steam API key is invalid.

    Args:
        steam_id_64 (str): The Steam ID 64 to get the owned games for.
        steam_api_key (str): The Steam API key to use to make the request.

    Raises:
        AuthFailedError: Raised if a 401 is received when trying to look up the
        owned games for the user. May be due to an invalid Steam API key or due
        to a non-public profile that the key does not have access to view.

    Returns:
        list[OwnedGame]: A list of owned games, including only the name,
        playtime, and appid. See definition of ``OwnedGame`` for the exact
        property names.
    """
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={steam_api_key}&steamid={steam_id_64}&include_appinfo=1"
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        parsed_json = {}
        try:
            async with session.get(url) as response:
                json_text = await response.text()
                parsed_json = json.loads(json_text)
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise AuthFailedError(
                    f'Could not retrieve games for SteamID64 "{steam_id_64}"'
                )

    if "response" not in parsed_json:
        return []
    if "games" not in parsed_json["response"]:
        return []
    owned_games: list[OwnedGame] = [
        {
            "name": game["name"],
            "playtime_forever": game["playtime_forever"],
            "appid": game["appid"],
        }
        for game in parsed_json["response"]["games"]
    ]
    return owned_games
