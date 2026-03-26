import argparse
import requests
import sys
from bs4 import BeautifulSoup

# Force utf-8 encoding for standard output to avoid Windows console errors
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_etymology(word, language='English'):
    url = f"https://en.wiktionary.org/wiki/{word}"
    headers = {'User-Agent': 'EtymologyFetcher/1.0 (Python)'}
    
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Wiktionary: {e}"
        
    if response.status_code == 404:
        return f"Error: Word '{word}' not found on Wiktionary."
    elif response.status_code != 200:
        return f"Error: Failed to fetch data. HTTP Status {response.status_code}."
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Format the language string to match Wiktionary section IDs (e.g. "old english" -> "Old_English")
    language_id = language.title().replace(' ', '_')
    
    # Find the language section using its id
    lang_header = soup.find(id=language_id)
    if not lang_header:
        return f"Error: Language '{language}' not found for the word '{word}'."
        
    # The id is often on a span inside the h2, or the h2 itself. 
    lang_block = lang_header
    while lang_block and lang_block.name not in ['h2']:
        lang_block = lang_block.parent
    
    if not lang_block:
         return f"Error: Could not locate language section properly for '{language}'."

    # In modern Wikipedia skins, headings are wrapped in <div class="mw-heading">
    if lang_block.parent and lang_block.parent.name == 'div' and 'mw-heading' in lang_block.parent.get('class', []):
        lang_block = lang_block.parent

    etymologies = []
    current_etymology = []
    recording = False
    
    for sibling in lang_block.next_siblings:
        # Skip NavigableStrings (newlines, spaces)
        if not sibling.name:
            continue
            
        # Check if sibling is a header or wrapped header
        heading_tag = None
        if sibling.name in ['h2', 'h3', 'h4', 'h5']:
            heading_tag = sibling
        elif sibling.name == 'div' and 'mw-heading' in sibling.get('class', []):
            heading_tag = sibling.find(['h2', 'h3', 'h4', 'h5'])
            
        if heading_tag:
            # Reached next language section
            if heading_tag.name == 'h2':
                break
                
            headline_text = heading_tag.get_text(strip=True).replace('[edit]', '').strip()
            
            if headline_text.startswith('Etymology'):
                if current_etymology:
                    etymologies.append('\n'.join(current_etymology))
                    current_etymology = []
                recording = True
            else:
                if recording and current_etymology:
                    etymologies.append('\n'.join(current_etymology))
                    current_etymology = []
                recording = False
                
        # Collect paragraphs and lists if we are recording an etymology
        elif recording and sibling.name in ['p', 'ul', 'ol', 'div']:
            # Sometimes etymologies have divs (e.g. for quotes, but ignore huge structural divs)
            # Safe bet is p, ul, ol
            if sibling.name in ['p', 'ul', 'ol']:
                text = sibling.get_text(separator=' ', strip=True)
                if text:
                    current_etymology.append(text)
                
    # Append the last recorded etymology if we ended without spotting a new heading
    if current_etymology:
        etymologies.append('\n'.join(current_etymology))
        
    if not etymologies:
        return f"No etymology found for '{word}' in '{language}'."
        
    # Format the output cleanly
    if len(etymologies) == 1:
        return f"Etymology of '{word}' ({language}):\n\n{etymologies[0]}\n"
    else:
        output = [f"Etymology of '{word}' ({language}):"]
        for i, ety in enumerate(etymologies, 1):
            output.append(f"\n[Etymology {i}]")
            output.append(ety)
        return "\n".join(output) + "\n"

def main():
    parser = argparse.ArgumentParser(description="Fetch the etymology of a word from Wiktionary.")
    parser.add_argument("word", help="The word to search for.")
    parser.add_argument("-l", "--language", default="English", help="The language of the word (default: English).")
    
    args = parser.parse_args()
    
    result = get_etymology(args.word, args.language)
    print(result)

if __name__ == "__main__":
    main()
