# main.py
from scraper import scrape_post
import json
import os
import requests

def main():
    shortcode = "DH8YiT3IiqP"  # Změň podle potřeby

    try:
        post_data = scrape_post(shortcode)
    except Exception as e:
        print(str(e))
        return

    print("\n📦 Extrahovaná data:")
    print(json.dumps(post_data, indent=2, ensure_ascii=False))

    # Uložení do JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(post_data, f, indent=2, ensure_ascii=False)
    print("💾 Data byla uložena do data.json")

    # Stažení média
    media_type = ".mp4" if post_data["is_video"] else ".jpg"
    filename = f"{shortcode}_media{media_type}"
    response = requests.get(post_data["media_url"])

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Médium bylo uloženo jako {filename}")
    else:
        print(f"❌ Chyba při stahování média: HTTP {response.status_code}")

if __name__ == "__main__":
    main()
