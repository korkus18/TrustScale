import re
import json
from urllib.parse import quote, urlparse
import requests
from app.models.post import Post, Author, CarouselItem, Location
from app.constants import (
    INSTAGRAM_API_URL,
    INSTAGRAM_MEDIA_ENDPOINT,
    INSTAGRAM_MEDIA_DETAILS_ENDPOINT,
    HEADERS
)


class Scraper:
    """Class for scraper using Instagram Basic Display API

    Raises:
        ValueError: Raised when URL is invalid or response parsing fails
        requests.RequestException: Raised when request fails
    """

    def __init__(self, access_token: str):
        """Initialize scraper with Instagram access token

        Args:
            access_token (str): Instagram Basic Display API access token
        """
        self.access_token = access_token

    def _extract_media_id(self, url: str) -> str:
        """Extract media ID from Instagram URL

        Args:
            url (str): Instagram post URL

        Returns:
            str: Media ID

        Raises:
            ValueError: If URL is invalid or media ID cannot be extracted
        """
        try:
            # Parse URL and get path
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Handle different URL formats
            if 'p' in path_parts:
                # Handle /p/SHORTCODE format
                shortcode = path_parts[path_parts.index('p') + 1]
            else:
                # Handle /username/posts/SHORTCODE format
                shortcode = path_parts[-1]
            
            if not shortcode:
                raise ValueError("Invalid Instagram URL: Could not extract shortcode")
                
            # Convert shortcode to media ID
            # This is a simplified version - in production, you'd need to implement
            # the actual conversion algorithm or use a different endpoint
            return shortcode
            
        except Exception as e:
            raise ValueError(f"Invalid Instagram URL: {str(e)}")

    def map_instagram_response(self, data: dict) -> Post:
        """Maps Instagram Basic Display API response to Post datatype structure

        Args:
            data (dict): Response from Instagram API as dictionary

        Returns:
            Post: Custom datatype Post

        Raises:
            ValueError: If response data is invalid or missing required fields
        """
        try:
            print("📦 Received data structure:", json.dumps(data, indent=2))
            
            if not data.get("id"):
                print("❌ No 'id' field in response")
                raise ValueError("Invalid response from Instagram: Missing 'id' field")

            # Extract hashtags from caption
            caption_text = data.get("caption", "")
            hashtags = re.findall(r"#(\w+)", caption_text)

            # Create author object
            author = Author(
                username=data.get("username", "unknown"),
                full_name=data.get("username", "Unknown User"),
                id=data.get("id", "0")
            )

            # Create location object if available
            location_info = data.get("location", {})
            location = Location(
                name=location_info.get("name"),
                lat=location_info.get("latitude"),
                lng=location_info.get("longitude")
            )

            # Handle carousel items if present
            carousel = []
            if "children" in data:
                for child in data["children"]["data"]:
                    carousel.append(CarouselItem(
                        media_url=child.get("media_url"),
                        is_video=child.get("media_type") == "VIDEO",
                        accessibility_caption=child.get("caption")
                    ))

            # Create post object
            post = Post(
                author=author,
                caption=caption_text,
                hashtags=hashtags,
                media_url=data.get("media_url"),
                is_video=data.get("media_type") == "VIDEO",
                timestamp=data.get("timestamp"),
                like_count=data.get("like_count", 0),
                comment_count=data.get("comments_count", 0),
                accessibility_caption=data.get("caption"),
                location=location,
                tagged_users=[],  # Basic Display API doesn't provide this
                carousel=carousel if carousel else None
            )
            
            print("✅ Successfully mapped response to Post object")
            return post

        except KeyError as e:
            print(f"❌ KeyError: {str(e)}")
            raise ValueError(f"Invalid response structure: Missing key {str(e)}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            raise ValueError(f"Error parsing Instagram response: {str(e)}")

    def scrape(self, url: str) -> Post:
        """Scrapes data from Instagram using Basic Display API

        Args:
            url (str): URL of Instagram post

        Raises:
            ValueError: If URL is invalid or response parsing fails
            requests.RequestException: If request fails

        Returns:
            Post: Returns data with type Post which is used in Analyzer
        """
        media_id = self._extract_media_id(url)
        print(f"🔍 Extracted media ID: {media_id}")

        # Prepare request URL with access token
        request_url = INSTAGRAM_MEDIA_DETAILS_ENDPOINT.format(media_id=media_id)
        params = {
            "access_token": self.access_token,
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,children{media_url,media_type,caption}"
        }

        print(f"📡 Sending request to Instagram API for media ID: {media_id}")
        print(f"🔑 Request URL: {request_url}")
        print(f"🔑 Parameters: {json.dumps(params, indent=2)}")

        try:
            response = requests.get(
                request_url,
                params=params,
                headers=HEADERS,
                timeout=30
            )
            
            print(f"📥 Response status code: {response.status_code}")
            print(f"📥 Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            try:
                data = response.json()
                print(f"📦 Raw response data: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {str(e)}")
                print(f"📄 Raw response text: {response.text}")
                raise ValueError(f"Invalid JSON response from Instagram: {str(e)}")

            return self.map_instagram_response(data)

        except requests.RequestException as e:
            print(f"❌ Request error: {str(e)}")
            raise ValueError(f"Failed to fetch data from Instagram: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            raise ValueError(f"Unexpected error during scraping: {str(e)}")
