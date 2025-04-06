# scraper.py
import json
import httpx
import re
from urllib.parse import quote

INSTAGRAM_DOCUMENT_ID = "8845758582119845"

def scrape_post(shortcode: str):
    client = httpx.Client(
        headers={
            "x-ig-app-id": "936619743392459",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.instagram.com/",
        },
        timeout=30,
    )

    variables = quote(json.dumps({
        'shortcode': shortcode,
        'fetch_tagged_user_count': None,
        'hoisted_comment_id': None,
        'hoisted_reply_id': None
    }, separators=(',', ':')))

    body = f"variables={variables}&doc_id={INSTAGRAM_DOCUMENT_ID}"
    url = "https://www.instagram.com/graphql/query"

    print(f" Posílám request na Instagram API pro shortcode: {shortcode}")
    result = client.post(url=url, data=body)

    if result.status_code != 200:
        raise Exception(f" Chyba HTTP: {result.status_code}")

    data = json.loads(result.text)
    media = data.get("data", {}).get("xdt_shortcode_media", None)
    if not media:
        raise Exception(" Nepodařilo se najít data příspěvku.")

    caption = media.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "")
    hashtags = re.findall(r"#(\w+)", caption)

    # Owner
    owner = media.get("owner", {})
    author_info = {
        "username": owner.get("username"),
        "full_name": owner.get("full_name"),
        "id": owner.get("id")
    }

    # Engagement
    likes = media.get("edge_media_preview_like", {}).get("count")
    comments = media.get("edge_media_to_comment", {}).get("count")

    # Accessibility
    alt_text = media.get("accessibility_caption")

    # Location
    location = media.get("location")
    location_info = {
        "name": location.get("name") if location else None,
        "lat": location.get("lat") if location else None,
        "lng": location.get("lng") if location else None
    }

    # Carousel
    carousel = []
    if media.get("edge_sidecar_to_children"):
        for edge in media["edge_sidecar_to_children"]["edges"]:
            node = edge.get("node", {})
            carousel.append({
                "media_url": node.get("video_url") or node.get("display_url"),
                "is_video": node.get("is_video"),
                "accessibility_caption": node.get("accessibility_caption")
            })

    output = {
        "author": author_info,
        "caption": caption,
        "hashtags": hashtags,
        "media_url": media.get("video_url") or media.get("display_url"),
        "is_video": media.get("is_video"),
        "timestamp": media.get("taken_at_timestamp"),
        "like_count": likes,
        "comment_count": comments,
        "accessibility_caption": alt_text,
        "location": location_info,
        "carousel": carousel if carousel else None
    }

    return output
