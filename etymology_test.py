import sys
from wiktionaryparser import WiktionaryParser

def get_etymology(word, language='english'):
    parser = WiktionaryParser()
    parser.set_default_language(language)
    try:
        data = parser.fetch(word)
        if not data:
            return f"No data found for '{word}' in '{language}'."
        
        etymologies = []
        for i, entry in enumerate(data):
            if 'etymology' in entry and entry['etymology']:
                etymologies.append(f"Etymology {i+1}:\n{entry['etymology']}")
                
        if etymologies:
            return "\n\n".join(etymologies)
        else:
            return f"No etymology found for '{word}' in '{language}'."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python etymology.py <word> [language]")
        sys.exit(1)
        
    word = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'english'
    
    print(get_etymology(word, language))
