# main.py
from scraper import scrape_post
import json
import os
import requests

def main():
    shortcode = "DIG9r12pVc6"  # Změň podle potřeby

    try:
        post_data = scrape_post(shortcode)
    except Exception as e:
        print(str(e))
        return

    print("\n Extrahovaná data:")
    print(json.dumps(post_data, indent=2, ensure_ascii=False))

    # Cesta do složky scrapers/<shortcode>/
    output_dir = os.path.join("scrapers", shortcode)
    os.makedirs(output_dir, exist_ok=True)

    # Uložení JSON
    json_path = os.path.join(output_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(post_data, f, indent=2, ensure_ascii=False)
    print(f" Uloženo: {json_path}")

    # Stažení média
    media_type = ".mp4" if post_data["is_video"] else ".jpg"
    media_filename = f"media{media_type}"
    media_path = os.path.join(output_dir, media_filename)

    response = requests.get(post_data["media_url"])
    if response.status_code == 200:
        with open(media_path, "wb") as f:
            f.write(response.content)
        print(f" Médium uloženo jako: {media_path}")
    else:
        print(f" Chyba při stahování média: HTTP {response.status_code}")

if __name__ == "__main__":
    main()
