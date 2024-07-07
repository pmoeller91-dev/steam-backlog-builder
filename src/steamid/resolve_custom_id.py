import aiohttp
import defusedxml
import defusedxml.ElementTree


def steam_community_id_url(id: str) -> str:
    """Just formats a custom ID into a URL that can be used to look it up.

    Args:
        id (str): The custom ID to format

    Returns:
        str: A URL to the Steam Community for that custom id, with the
        ``?xml=1`` specifier included, to prompt an XML response.
    """
    return f"https://steamcommunity.com/id/{id}?xml=1"


class InvalidCustomIDError(Exception):
    """Thrown when the custom ID can't be associated with a Steam profile.
    Happens when the xml response contains no valid ``steamID64`` element or if
    the response from ``steamcommunity.com`` is ``404``.
    """

    pass


async def resolve_custom_id(id: str) -> str:
    """Resolves a custom Steam community ID to its associated Steam ID 64 using
    the xml returned by the Steam Community site.

    Args:
        id (str): The custom Steam community ID to resolve

    Raises:
        NoSteamIDError: Raised if the XML contains no ``steamID64`` element, or
        if the element is blank.
        InvalidCustomIDError: Raised if the custom id is not associated with a
        steam profile.
        aiohttp.ClientResponseError: Raised if the request made to
        ``steamcommunity.com`` is not a success status.

    Returns:
        str: The resolved Steam ID 64
    """
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        try:
            async with session.get(steam_community_id_url(id)) as response:
                xml_text = await response.text()
                etree = defusedxml.ElementTree.fromstring(xml_text)
                steam_id_64_element = etree.find("steamID64")
                if steam_id_64_element is None:
                    raise InvalidCustomIDError(
                        "steamID64 element could not be found in returned XML document"
                    )
                if not steam_id_64_element.text:
                    raise InvalidCustomIDError("steamID64 element was blank")
                return steam_id_64_element.text
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise InvalidCustomIDError(
                    f"The custom id {id} is not associated with a Steam profile."
                )
            raise e
