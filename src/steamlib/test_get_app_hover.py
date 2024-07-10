import unittest
from aioresponses import aioresponses
from .get_app_hover import get_app_hover
import json
from .error import InvalidResponseError

valid_response = {
    "strReleaseDate": "Released: Oct 17, 2013",
    "strDescription": "The Stanley Parable is a first person exploration game. You will play as Stanley, and you will not play as Stanley. You will follow a story, you will not follow a story. You will have a choice, you will have no choice. The game will end, the game will never end.",
    "rgScreenshots": [
        {
            "appid": 221910,
            "id": 0,
            "filename": "ss_49e682563292992309e3047f30128f3dba4c39ce.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 1,
            "filename": "ss_7b119bfff7ebfbcd86c1af1210bdac8666ab4ae8.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 2,
            "filename": "ss_523aa042385c6b1c8f6c9870ecffef18627d9064.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 3,
            "filename": "ss_0411c36ac2bdc3f22d642ec09d9f417e6902044d.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 4,
            "filename": "ss_8905426b3f0ec7efd3c07f053d0276ced38a1f8f.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 5,
            "filename": "ss_18d2adf006de1720ac744348f4fb3b7e392b4968.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 6,
            "filename": "ss_4562a1cb6aa65cbf8746780d65414157f949dcee.jpg",
            "all_ages": "",
        },
        {
            "appid": 221910,
            "id": 7,
            "filename": "ss_a503d355053ab9547ae30e85313055ced4d589a4.jpg",
            "all_ages": "1",
        },
    ],
    "rgCategories": [{"strDisplayName": "Single-player"}],
    "strGenres": "Adventure, Indie",
    "strMicroTrailerURL": "https://cdn.akamai.steamstatic.com/steam/apps/2029779/microtrailer.webm?t=1447359219",
    "ReviewSummary": {
        "strReviewSummary": "Very Positive",
        "cReviews": 39046,
        "cRecommendationsPositive": 36101,
        "cRecommendationsNegative": 2945,
        "nReviewScore": 8,
    },
}


class TestGetAppHover(unittest.IsolatedAsyncioTestCase):
    @aioresponses()
    async def test_request(self, mocked):
        test_appid = 12345
        expected_response = valid_response
        mocked.get(
            f"https://store.steampowered.com/apphoverpublic/{test_appid}/?l=english&json=1",
            status=200,
            body=json.dumps(expected_response),
        )
        response = await get_app_hover(test_appid)
        self.assertEqual(response, expected_response)

    @aioresponses()
    async def test_request_error_code(self, mocked):
        test_appid = 12345
        expected_response = valid_response
        mocked.get(
            f"https://store.steampowered.com/apphoverpublic/{test_appid}/?l=english&json=1",
            status=404,
            body=json.dumps(expected_response),
        )
        with self.assertRaises(InvalidResponseError):
            await get_app_hover(test_appid)

    @aioresponses()
    async def test_invalid_response(self, mocked):
        test_appid = 12345
        invalid_response = {"error": "some error"}
        mocked.get(
            f"https://store.steampowered.com/apphoverpublic/{test_appid}/?l=english&json=1",
            status=200,
            body=json.dumps(invalid_response),
        )
        with self.assertRaises(InvalidResponseError):
            await get_app_hover(test_appid)


if __name__ == "__main__":
    unittest.main()
