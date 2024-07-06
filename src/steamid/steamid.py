from enum import Enum
import re


class SteamIDType(Enum):
    STEAM_ID = "STEAM_ID"  # STEAM_0:0:11101
    STEAM_ID_3 = "Steam_ID3"  # U:1:22202 or [U:1:22202]
    STEAM_ID_64 = "STEAM_64"  # 76561197960287930
    CUSTOM_NAME = "CUSTOM"  # gabelogannewell
    CUSTOM_URL = "CUSTOM_URL"  # https://steamcommunity.com/id/gabelogannewell
    STANDARD_URL = (
        "STANDARD_URL"  # https://steamcommunity.com/profiles/76561197960287930
    )


steam_id_64_identifier = 0x0110000100000000  # SteamID64 identifier for individual accounts, see: https://developer.valvesoftware.com/wiki/SteamID

steam_id_regex = {
    SteamIDType.STEAM_ID: r"STEAM_(\d):(\d):(\d+)",
    SteamIDType.STEAM_ID_3: r"\[?U:(\d):(\d+)\]?",  # Allows unbalanced brackets, but easier
    SteamIDType.STEAM_ID_64: r"(\d{17})",
    SteamIDType.CUSTOM_NAME: r"(.+)",  # Must be checked last, as almost anything can be a custom name
    SteamIDType.CUSTOM_URL: r"https?://steamcommunity\.com/id/([^/]+)(?:/.*)?",
    SteamIDType.STANDARD_URL: r"https?://steamcommunity\.com/profiles/(\d{17})(?:/.*)?",
}


class SteamID:
    """Represents a SteamID, and allows converting between various formats to
    SteamID64.

    Raises:
        ValueError: Raised if an empty string is provided to the constructor, or
        if no format matches the provided string.
    """

    def __init__(self, steam_id: str) -> None:
        """Creates a new SteamID using the given string. Accepts SteamIDv1,
        SteamIDv3, SteamID64, Custom Names, Full Steam Community URLs with
        SteamID64, and Full Steam Community URLs with Custom Names.

        Args:
            steam_id (str): The string to attempt to identify as a Steam ID
        """
        self._steam_id = self._identify_steam_id(steam_id)
        self._steam_id_64: str | None = None

    def _identify_steam_id(self, steam_id: str) -> tuple[SteamIDType, str]:
        """Accepts a string and attempts to determine what format of SteamID it
        is. Any non-empty string will ultimately be identified as a custom name
        if no other format matches.

        Args:
            steam_id (str): The string to attempt to identify as a Steam ID

        Raises:
            ValueError: Raised if an empty string is provided or if no other
            format matches.

        Returns:
            tuple[SteamIDType, str]: The type of the SteamID and the string that matched.
        """
        stripped_steam_id = steam_id.strip()
        if re.match(steam_id_regex[SteamIDType.STEAM_ID], stripped_steam_id):
            return (SteamIDType.STEAM_ID, stripped_steam_id)
        if re.match(steam_id_regex[SteamIDType.STEAM_ID_3], stripped_steam_id):
            return (SteamIDType.STEAM_ID_3, stripped_steam_id.strip("[]"))
        if re.match(steam_id_regex[SteamIDType.STEAM_ID_64], stripped_steam_id):
            return (SteamIDType.STEAM_ID_64, stripped_steam_id)
        if re.match(steam_id_regex[SteamIDType.STANDARD_URL], stripped_steam_id):
            return (SteamIDType.STANDARD_URL, stripped_steam_id)
        if re.match(steam_id_regex[SteamIDType.CUSTOM_URL], stripped_steam_id):
            return (SteamIDType.CUSTOM_URL, stripped_steam_id)
        if re.match(steam_id_regex[SteamIDType.CUSTOM_NAME], stripped_steam_id):
            return (SteamIDType.CUSTOM_NAME, stripped_steam_id)

        raise ValueError("Invalid Steam ID format!")

    async def to_steam_id_64(self) -> str:
        """Converts a Steam ID to a Steam ID 64 representation. May need to make
        a web request to convert custom names and custom URLs to the correct
        representation. This request will only be made once per Steam ID if needed
        and the result will be cached.

        Raises:
            NotImplementedError: Raised for Custom Name and Custom URL as this
            is not implemented yet

        Returns:
            str: The Steam ID 64 representation.
        """
        if self._steam_id_64 is not None:
            return self._steam_id_64

        match self._steam_id[0]:
            case SteamIDType.STEAM_ID:
                matches = re.match(
                    steam_id_regex[SteamIDType.STEAM_ID], self._steam_id[1]
                )
                y = int(matches.group(2))
                z = int(matches.group(3))

                steam_id_64 = z * 2 + steam_id_64_identifier + y
                self._steam_id_64 = str(steam_id_64)

            case SteamIDType.STEAM_ID_3:
                matches = re.match(
                    steam_id_regex[SteamIDType.STEAM_ID_3], self._steam_id[1]
                )
                w = int(matches.group(2))
                steam_id_64 = w + steam_id_64_identifier
                self._steam_id_64 = str(steam_id_64)
            case SteamIDType.STEAM_ID_64:
                self._steam_id_64 = self._steam_id[1]
            case SteamIDType.STANDARD_URL:
                matches = re.match(
                    steam_id_regex[SteamIDType.STANDARD_URL], self._steam_id[1]
                )
                self._steam_id_64 = matches.group(1)
            case SteamIDType.CUSTOM_URL:
                raise NotImplementedError("Custom URL not implemented")
            case SteamIDType.CUSTOM_NAME:
                raise NotImplementedError("Custom name not implemented")

        return self._steam_id_64
