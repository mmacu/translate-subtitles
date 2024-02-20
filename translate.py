import os
import ass
import requests
from dotenv import load_dotenv
from tqdm import tqdm
import argparse

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

def translate_file(input_file):
    with open(input_file, encoding='utf-8') as f:
        subs = ass.parse(f)

    # Extracting the base name without extension and adding "(pl)"
    output_file = os.path.splitext(input_file)[0] + "(pl).ass"

    translate_subs(subs, target_language='pl')

    with open(output_file, 'w', encoding='utf_8_sig') as f:
        subs.dump_file(f)

def main():
    parser = argparse.ArgumentParser(description='Translate subtitles to another language.')
    parser.add_argument('input_files', nargs='+', help='Path(s) to the input subtitle file(s)')

    args = parser.parse_args()
    input_files = args.input_files

    for input_file in input_files:
        translate_file(input_file)

if __name__ == "__main__":
    main()
