import json
import httpx
import re
from urllib.parse import quote

INSTAGRAM_DOCUMENT_ID = "8845758582119845"  # ID pro příspěvky

def scrape_post(shortcode: str):
    client = httpx.Client(
        headers={
            "x-ig-app-id": "936619743392459",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
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

    print(f"📡 Posílám request na Instagram API pro shortcode: {shortcode}")
    result = client.post(url=url, data=body)

    if result.status_code != 200:
        raise Exception(f"❌ Chyba HTTP: {result.status_code}")

    data = json.loads(result.text)

    # Ověř, že data obsahují potřebná pole
    media = data.get("data", {}).get("xdt_shortcode_media", None)
    if not media:
        raise Exception("❌ Nepodařilo se najít data příspěvku.")

    caption = media.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "")

    output = {
        "author": media["owner"]["username"],
        "caption": caption,
        "hashtags": re.findall(r"#(\w+)", caption),
        "media_url": media.get("display_url") if not media.get("is_video") else media.get("video_url"),
        "is_video": media.get("is_video"),
        "timestamp": media.get("taken_at_timestamp")
    }

    return output

# --- hlavní část ---
if __name__ == "__main__":
    shortcode = "DH8YiT3IiqP"  # shortcode tvého postu
    post_data = scrape_post(shortcode)

    print("\n📄 Extrahovaná data o příspěvku:")
    print(json.dumps(post_data, indent=2))

    # Stažení média
    import requests
    media_type = ".mp4" if post_data["is_video"] else ".jpg"
    filename = f"{shortcode}_media{media_type}"
    response = requests.get(post_data["media_url"])

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"\n✅ Médium úspěšně uloženo jako {filename}")
    else:
        print(f"\n❌ Chyba při stahování média: HTTP {response.status_code}")
