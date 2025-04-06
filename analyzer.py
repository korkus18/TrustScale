# analyzer.py
from openai import OpenAI
import json
import os


api_key = os.getenv("OPENAI_API_KEY") or "sk..."  # Změň nebo načítej bezpečně

client = OpenAI(api_key=api_key)

def analyze_post(data: dict) -> str:
    prompt = """Zhodnoť, prosím, tento Instagramový příspěvek na základě následujících kategorií:

Engagement – lajky, komentáře, sdílení, uložení, čas u příspěvku (pokud dostupné)

Kvalita a relevance obsahu – vizuální úroveň, styl, téma, smysluplnost a struktura captionu, použití klíčových slov

Chování sledujících a komunity – síla vztahu mezi autorem a publikem (pokud lze odvodit), interakce

Technické a distribuční faktory – typ formátu, počet a struktura carouselu, přítomnost tagů, lokace, využití funkcí IG

Negativní signály – možné problémy s algoritmem (např. clickbait, shadowban rizika, nevhodný obsah)

Vstupní data najdeš v přiloženém JSON souboru ve struktuře odpovídající Instagramovému API.

Výstup prosím rozděl podle výše uvedených kategorií. U každé oblasti napiš, co funguje dobře a co by mohlo být zlepšeno."""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Jsi analytik sociálních sítí. Zhodnoť data z Instagramu."},
            {"role": "user", "content": f"{prompt}\n\nData:\n{json.dumps(data, indent=2)}"}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
