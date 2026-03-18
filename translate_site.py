import os
import glob
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor

# Folders to generate
LANGS = {
    'zh-cn': GoogleTranslator(source='en', target='zh-CN'),
    'zh-tw': GoogleTranslator(source='en', target='zh-TW')
}

html_files = glob.glob('*.html')
for lang in LANGS:
    os.makedirs(lang, exist_ok=True)

BLOCK_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'button', 'a', 'label', 'summary', 'blockquote']

def translate_nodes(nodes_dict, translator):
    to_translate = [k for k, v in nodes_dict.items() if v is None]
    if not to_translate:
        return
        
    def fetch_translation(text):
        try:
            return text, translator.translate(text)
        except Exception as e:
            return text, text

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_translation, to_translate)
        for original, translated in results:
            nodes_dict[original] = translated

cache_cn = {}
cache_tw = {}

for lang_dir, translator in LANGS.items():
    print(f"--- Translating to {lang_dir} ---")
    cache = cache_cn if lang_dir == 'zh-cn' else cache_tw
    
    for file in html_files:
        print(f"Processing {file}...")
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # 1. Fix asset paths
        for tag in soup.find_all(['img', 'script', 'link']):
            if tag.name == 'img' and tag.has_attr('src'):
                if tag['src'].startswith('images/'):
                    tag['src'] = '../' + tag['src']
            elif tag.name == 'link' and tag.has_attr('href'):
                if tag['href'].startswith('images/'):
                    tag['href'] = '../' + tag['href']

        # 2. Extract texts to translate
        def is_translatable(tag):
            if tag.name not in BLOCK_TAGS and tag.name not in ['div', 'span']: return False
            texts = [s for s in tag.find_all(string=True, recursive=False) if s.strip()]
            if not texts and tag.name not in BLOCK_TAGS: return False
            for child in tag.children:
                if child.name in BLOCK_TAGS or child.name == 'div': return False
            return True

        tags_to_translate = []
        for tag in soup.find_all():
            if is_translatable(tag):
                inner_html = tag.decode_contents().strip()
                if not inner_html or inner_html.isnumeric(): continue
                if tag.name == 'span' and 'material-symbols-outlined' in tag.get('class', []): continue
                tags_to_translate.append((tag, inner_html))
                if inner_html not in cache:
                    cache[inner_html] = None

        loose_texts = []
        for element in soup.find_all(string=True):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta']: continue
            text = element.strip()
            if text and len(text) > 1 and not text.isnumeric():
                loose_texts.append((element, text))
                if text not in cache:
                    cache[text] = None

        if soup.title and soup.title.string:
            title_text = soup.title.string.strip()
            if title_text not in cache:
                cache[title_text] = None

        # 3. Translate missing cache concurrently
        translate_nodes(cache, translator)

        # 4. Apply translations
        for tag, inner_html in tags_to_translate:
            translated = cache.get(inner_html) or inner_html
            tag.clear()
            tag.append(BeautifulSoup(translated, 'html.parser'))

        for element, text in loose_texts:
            translated = cache.get(text) or text
            try:
                element.replace_with(element.replace(text, translated))
            except ValueError:
                pass

        if soup.title and soup.title.string:
            title_text = soup.title.string.strip()
            translated = cache.get(title_text) or title_text
            soup.title.string = translated

        # Save file
        out_path = os.path.join(lang_dir, file)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
print("Translation complete.")
