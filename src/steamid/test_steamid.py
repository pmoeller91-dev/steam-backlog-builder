import unittest
from unittest.mock import patch, AsyncMock
from .steamid import SteamID, SteamIDType


class TestCreateSteamID(unittest.TestCase):
    def test_steamid(self):
        steam_id_string = "STEAM_0:0:11101"
        expected_steam_id = (SteamIDType.STEAM_ID, steam_id_string)
        steam_id = SteamID(steam_id_string)
        self.assertEqual(steam_id._steam_id, expected_steam_id)

    def test_steamid_3(self):
        steam_id_string = "[U:1:22202]"
        expected_steam_id = (SteamIDType.STEAM_ID_3, "U:1:22202")
        steam_id = SteamID(steam_id_string)
        self.assertEqual(steam_id._steam_id, expected_steam_id)

    def test_steamid_64(self):
        steam_id_string = "76561197960287930"
        expected_steam_id = (SteamIDType.STEAM_ID_64, steam_id_string)
        steam_id = SteamID(steam_id_string)
        self.assertEqual(steam_id._steam_id, expected_steam_id)

    def test_steamid_standard_url(self):
        steam_id_string = "https://steamcommunity.com/profiles/76561197960287930"
        expected_steam_id = (SteamIDType.STANDARD_URL, steam_id_string)
        steam_id = SteamID(steam_id_string)
        self.assertEqual(steam_id._steam_id, expected_steam_id)

    def test_steamid_custom_url(self):
        steam_id_string = "https://steamcommunity.com/id/gabelogannewell"
        expected_steam_id = (SteamIDType.CUSTOM_URL, steam_id_string)
        steam_id = SteamID(steam_id_string)
        self.assertEqual(steam_id._steam_id, expected_steam_id)

    def test_steamid_custom_name(self):
        steam_id_string = "gabelogannewell"
        expected_steam_id = (SteamIDType.CUSTOM_NAME, steam_id_string)
        steam_id = SteamID(steam_id_string)
        self.assertEqual(steam_id._steam_id, expected_steam_id)

    def test_steamid_invalid(self):
        steam_id_string = ""
        self.assertRaises(ValueError, lambda: SteamID(steam_id_string))


class TestToSteamID64(unittest.IsolatedAsyncioTestCase):
    async def test_steam_id(self):
        steam_id_string = "STEAM_0:0:11101"
        expected_steam_id_64 = "76561197960287930"
        steam_id = SteamID(steam_id_string)
        steam_id_64 = await steam_id.to_steam_id_64()
        self.assertEqual(expected_steam_id_64, steam_id_64)

    async def test_steam_id_3(self):
        steam_id_string = "[U:1:22202]"
        expected_steam_id_64 = "76561197960287930"
        steam_id = SteamID(steam_id_string)
        steam_id_64 = await steam_id.to_steam_id_64()
        self.assertEqual(expected_steam_id_64, steam_id_64)

    async def test_steam_id_64(self):
        steam_id_string = "76561197960287930"
        expected_steam_id_64 = "76561197960287930"
        steam_id = SteamID(steam_id_string)
        steam_id_64 = await steam_id.to_steam_id_64()
        self.assertEqual(expected_steam_id_64, steam_id_64)

    async def test_standard_url(self):
        steam_id_string = "https://steamcommunity.com/profiles/76561197960287930"
        expected_steam_id_64 = "76561197960287930"
        steam_id = SteamID(steam_id_string)
        steam_id_64 = await steam_id.to_steam_id_64()
        self.assertEqual(expected_steam_id_64, steam_id_64)

    @patch("steamid.steamid.resolve_custom_id")
    async def test_custom_url(self, mocked_resolve_custom_id: AsyncMock):
        steam_id_string = "https://steamcommunity.com/id/gabelogannewell"
        expected_steam_id_64 = "12345678901234567"
        mocked_resolve_custom_id.return_value = expected_steam_id_64
        steam_id = SteamID(steam_id_string)
        steam_id_64 = await steam_id.to_steam_id_64()
        mocked_resolve_custom_id.assert_called_with("gabelogannewell")
        self.assertEqual(expected_steam_id_64, steam_id_64)

    @patch("steamid.steamid.resolve_custom_id")
    async def test_custom_name(self, mocked_resolve_custom_id: AsyncMock):
        steam_id_string = "gabelogannewell"
        expected_steam_id_64 = "12345678901234567"
        mocked_resolve_custom_id.return_value = expected_steam_id_64
        steam_id = SteamID(steam_id_string)
        steam_id_64 = await steam_id.to_steam_id_64()
        mocked_resolve_custom_id.assert_called_with("gabelogannewell")
        self.assertEqual(expected_steam_id_64, steam_id_64)


if __name__ == "__main__":
    unittest.main()
