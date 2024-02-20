import os
import ass
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

deepl_api_key = os.getenv("DEEPL_API_KEY")

def translate_text(text, target_language):
    deepl_api_url = "https://api-free.deepl.com/v2/translate"

    params = {
        'auth_key': deepl_api_key,
        'text': text,
        'target_lang': target_language,
    }

    response = requests.post(deepl_api_url, data=params)

    if response.status_code == 200:
        translation = response.json()['translations'][0]['text']
        return translation
    else:
        print(f"Error translating text: {response.status_code}")
        return None

def translate_subs(subs, target_language):
    total_events = len(subs.events)
    with tqdm(total=total_events, desc='Translating Subtitles') as pbar:
        for event in subs.events:
            # Check if the event has text
            if event.text:
                # Translate the text to the target language
                translated_text = translate_text(event.text, target_language)

                # Update the event with the translated text
                if translated_text:
                    event.text = translated_text

            # Update the progress bar
            pbar.update(1)

def main():
    with open("english_subs.ass", encoding='utf-8') as f:
        subs = ass.parse(f)

    translate_subs(subs, target_language='pl')

    with open("polish_subs.ass", 'w', encoding='utf-8') as f:
        subs.dump_file(f)

if __name__ == "__main__":
    main()
