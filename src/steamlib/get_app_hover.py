from typing import TypedDict
import aiohttp
import json
from jsonschema import validate
from .error import InvalidResponseError

class AppHoverScreenshot(TypedDict):
    appid: int
    id: int
    filename: str
    all_ages: str
    
class AppHoverCategory(TypedDict):
    strDisplayName: str
    
class AppHoverReviewsSummary(TypedDict):
    strReviewsSummary: str
    cReviews: int
    cRecommendationsPositive: int
    cRecommendationsNegative: int
    nReviewScore: int

class AppHoverResponse(TypedDict):
    strReleaseDate: str
    strDescription: str
    rgScreenshots: list[AppHoverScreenshot]
    rgCategories: list[AppHoverCategory]
    strGenres: str
    strMicroTrailerURL: str
    ReviewSummary: AppHoverReviewsSummary

app_hover_response_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "strReleaseDate": {
      "type": "string"
    },
    "strDescription": {
      "type": "string"
    },
    "rgScreenshots": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "appid": {
            "type": "integer"
          },
          "id": {
            "type": "integer"
          },
          "filename": {
            "type": "string"
          },
          "all_ages": {
            "type": "string"
          }
        },
        "required": [
          "appid",
          "id",
          "filename",
          "all_ages"
        ]
      }
    },
    "rgCategories": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "strDisplayName": {
            "type": "string"
          }
        },
        "required": [
          "strDisplayName"
        ]
      }
    },
    "strGenres": {
      "type": "string"
    },
    "strMicroTrailerURL": {
      "type": "string"
    },
    "ReviewSummary": {
      "type": "object",
      "properties": {
        "strReviewSummary": {
          "type": "string"
        },
        "cReviews": {
          "type": "integer"
        },
        "cRecommendationsPositive": {
          "type": "integer"
        },
        "cRecommendationsNegative": {
          "type": "integer"
        },
        "nReviewScore": {
          "type": "integer"
        }
      },
      "required": [
        "strReviewSummary",
        "cReviews",
        "cRecommendationsPositive",
        "cRecommendationsNegative",
        "nReviewScore"
      ]
    }
  },
  "required": [
    "strReleaseDate",
    "strDescription",
    "rgScreenshots",
    "rgCategories",
    "strGenres",
    "strMicroTrailerURL",
    "ReviewSummary"
  ]
}

    
async def get_app_hover(appid: int) -> AppHoverResponse:
    """Gets the ``AppHoverResponse`` from the Steam store endpoint, for the given appid.

    Args:
        appid (int): The app id to retrieve the response for

    Raises:
        InvalidResponseError: Raised when an invalid response is received from
        the server, whether invalid JSON or a response that does not meet the
        expected schema.

    Returns:
        AppHoverResponse: The ``AppHoverResponse`` from the endpoint
    """
    url = f"https://store.steampowered.com/apphoverpublic/{appid}/?l=english&json=1"
    json_text = ""
    parsed_json: AppHoverResponse
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        try:
            async with session.get(url) as response:
                json_text = await response.text()
        except Exception as e:  
            raise InvalidResponseError from e
    try:
        parsed_json = json.loads(json_text)
        validate(instance=parsed_json, schema=app_hover_response_schema)
    except Exception as e:
        raise InvalidResponseError from e
    
    return parsed_json