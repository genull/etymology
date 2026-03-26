# Etymology Fetcher

A Python command-line tool that fetches the etymology of words directly from Wiktionary. It defaults to scraping the English etymology but supports querying any language available on the word's page. If the requested language is not found, the software will hint at which languages *are* available for that word.

## Requirements

Both `requests` and `beautifulsoup4` are required to parse the Wiktionary HTML.

```powershell
pip install requests beautifulsoup4
```

## Usage

```powershell
# Fetch the English etymology for a word
python etymology.py word

# Fetch the etymology for a word in a specific language
python etymology.py Gabriel -l French
python etymology.py word -l "Old English"
```

## Arguments

- `word` : The target word to fetch the etymology for.
- `-l`, `--language` : (Optional) The language of the word. Defaults to `English`. Handles multi-word languages like "Old English".
