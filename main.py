
from scraper import scrape_post
from analyzer import analyze_post
import json
import os

def main():
    shortcode = "DIG9r12pVc6"  # Změň podle potřeby

    # === 1. Scrapování IG postu ===
    try:
        post_data = scrape_post(shortcode)
    except Exception as e:
        print(str(e))
        return

    print("\n Extrahovaná data:")
    print(json.dumps(post_data, indent=2, ensure_ascii=False))

    # 2. Vytvoření složky scrapers/<shortcode>/
    output_dir = os.path.join("scrapers", shortcode)
    os.makedirs(output_dir, exist_ok=True)

    # 3. Uložení data.json
    json_path = os.path.join(output_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(post_data, f, indent=2, ensure_ascii=False)
    print(f" Uloženo: {json_path}")


"""
    # 4. Analýza přes GPT-4 
    try:
        gpt_response = analyze_post(post_data)
        analysis_path = os.path.join(output_dir, "analysis.json")
        with open(analysis_path, "w", encoding="utf-8") as f:
            json.dump({
                "response": gpt_response
            }, f, indent=2, ensure_ascii=False)
        print(f" Výstup z GPT-4 uložen do {analysis_path}")
    except Exception as e:
        print(f" Chyba během analýzy přes OpenAI: {str(e)}")
"""
if __name__ == "__main__":
    main()
