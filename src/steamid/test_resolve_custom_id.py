import unittest
from aioresponses import aioresponses
from steamid.resolve_custom_id import (
    resolve_custom_id,
    steam_community_id_url,
    InvalidCustomIDError,
)

mocked_response = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><profile>
    <steamID64>76561197960287930</steamID64>
    <steamID><![CDATA[Rabscuttle]]></steamID>
    <onlineState>offline</onlineState>
    <stateMessage><![CDATA[Offline]]></stateMessage>
    <privacyState>friendsonly</privacyState>
    <visibilityState>1</visibilityState>
    <avatarIcon><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426.jpg]]></avatarIcon>
    <avatarMedium><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426_medium.jpg]]></avatarMedium>
    <avatarFull><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426_full.jpg]]></avatarFull>
    <vacBanned>0</vacBanned>
    <tradeBanState>None</tradeBanState>
    <isLimitedAccount>0</isLimitedAccount>
</profile>"""

mocked_invalid_response_no_steamid64_element = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><profile>
    <steamID><![CDATA[Rabscuttle]]></steamID>
    <onlineState>offline</onlineState>
    <stateMessage><![CDATA[Offline]]></stateMessage>
    <privacyState>friendsonly</privacyState>
    <visibilityState>1</visibilityState>
    <avatarIcon><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426.jpg]]></avatarIcon>
    <avatarMedium><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426_medium.jpg]]></avatarMedium>
    <avatarFull><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426_full.jpg]]></avatarFull>
    <vacBanned>0</vacBanned>
    <tradeBanState>None</tradeBanState>
    <isLimitedAccount>0</isLimitedAccount>
</profile>"""

mocked_invalid_response_empty_steamid64_element = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><profile>
    <steamID64></steamID64>
    <steamID><![CDATA[Rabscuttle]]></steamID>
    <onlineState>offline</onlineState>
    <stateMessage><![CDATA[Offline]]></stateMessage>
    <privacyState>friendsonly</privacyState>
    <visibilityState>1</visibilityState>
    <avatarIcon><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426.jpg]]></avatarIcon>
    <avatarMedium><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426_medium.jpg]]></avatarMedium>
    <avatarFull><![CDATA[https://avatars.akamai.steamstatic.com/c5d56249ee5d28a07db4ac9f7f60af961fab5426_full.jpg]]></avatarFull>
    <vacBanned>0</vacBanned>
    <tradeBanState>None</tradeBanState>
    <isLimitedAccount>0</isLimitedAccount>
</profile>"""


class TestResolveCustomID(unittest.IsolatedAsyncioTestCase):
    async def test_success(self):
        test_id = "GabeLoganNewell"
        expected_id_64 = "76561197960287930"
        with aioresponses() as m:
            m.get(steam_community_id_url(test_id), status=200, body=mocked_response)
            id_64 = await resolve_custom_id(test_id)
        self.assertEqual(id_64, expected_id_64)

    async def test_not_found(self):
        test_id = "GabeLoganNewell"
        with aioresponses() as m:
            m.get(steam_community_id_url(test_id), status=404, body="404: Not Found")
            with self.assertRaises(InvalidCustomIDError) as e:
                await resolve_custom_id(test_id)

    async def test_no_steamid64_element(self):
        test_id = "GabeLoganNewell"
        with aioresponses() as m:
            m.get(
                steam_community_id_url(test_id),
                status=200,
                body=mocked_invalid_response_no_steamid64_element,
            )
            with self.assertRaises(InvalidCustomIDError) as e:
                await resolve_custom_id(test_id)

    async def test_empty_steamid64_element(self):
        test_id = "GabeLoganNewell"
        with aioresponses() as m:
            m.get(
                steam_community_id_url(test_id),
                status=200,
                body=mocked_invalid_response_empty_steamid64_element,
            )
            with self.assertRaises(InvalidCustomIDError) as e:
                await resolve_custom_id(test_id)


if __name__ == "__main__":
    unittest.main()
