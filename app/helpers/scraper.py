import re
import json
from urllib.parse import quote
import requests
from app.models.post import Post, Author, CarouselItem, Location
from app.constants import INSTAGRAM_DOCUMENT_ID, INSTAGRAM_URL, HEADERS


class Scraper:
    """Class for scraper

    Raises:
        http_error: Raised when request gives error

    """

    def __init__(self):
        pass

    def _parse_shortcode(self, url: str) -> str:
        """Returns shortcode for a post"""
        # https://www.instagram.com/p/DIGYx2ZMwFv/?img_index=1

        return url.split("/")[4]

    def map_instagram_response(self, data: dict) -> Post:
        """Maps instagram response to Post datapyte structure

        Args:
            data (dict): Response from instagram as dictionaty

        Returns:
            Post: Custom datatype Post
        """
        media = data["data"]["xdt_shortcode_media"]

        caption_text = media.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "")
        hashtags = re.findall(r"#(\w+)", caption_text)

        author = Author(
            username=media["owner"]["username"],
            full_name=media["owner"].get("full_name"),
            id=media["owner"]["id"]
        )

        location_info = media.get("location") or {}
        location = Location(
            name=location_info.get("name"),
            lat=location_info.get("lat"),
            lng=location_info.get("lng")
        )

        carousel = []
        if "edge_sidecar_to_children" in media:
            for edge in media["edge_sidecar_to_children"]["edges"]:
                node = edge["node"]
                carousel.append(CarouselItem(
                    media_url=node.get("video_url") or node.get("display_url"),
                    is_video=node["is_video"],
                    accessibility_caption=node.get("accessibility_caption")
                ))

        return Post(
            author=author,
            caption=caption_text,
            hashtags=hashtags,
            media_url=media.get("video_url") or media.get("display_url"),
            is_video=media["is_video"],
            timestamp=media["taken_at_timestamp"],
            like_count=media["edge_media_preview_like"]["count"],
            comment_count=media.get("edge_media_to_comment", {}).get("count"),
            accessibility_caption=media.get("accessibility_caption"),
            location=location,
            tagged_users=[],  # or parse from edge_media_to_tagged_user if needed
            carousel=carousel if carousel else None
        )

    def scrape(self, url: str) -> Post:
        """Scrapes data from  intstagram passes it to map_instagram_response

        Args:
            url (str): Url of instagram post

        Raises:
            http_error: Raised when request gives error

        Returns:
            Post: returns dat with type Post which is used in Analyzer
        """
        shortcode = self._parse_shortcode(url=url)

        # Prepare variables and encode
        variables = {
            "shortcode": shortcode,
            "fetch_tagged_user_count": None,
            "hoisted_comment_id": None,
            "hoisted_reply_id": None
        }
        encoded_variables = quote(json.dumps(variables, separators=(',', ':')))

        payload = f"variables={encoded_variables}&doc_id={INSTAGRAM_DOCUMENT_ID}"

        print(f"📡 Sending request to Instagram API for shortcode: {shortcode}")

        try:
            response = requests.post(
                INSTAGRAM_URL,
                data=payload,
                headers=HEADERS,
                timeout=30
            )

            return self.map_instagram_response(response.json())

        except requests.RequestException as http_error:
            raise http_error
