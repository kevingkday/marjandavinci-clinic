import os
import glob
from bs4 import BeautifulSoup

GA_SNIPPET = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R7WY6BTL19"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-R7WY6BTL19');
</script>
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # Check if GA tags already exist to avoid duplication
    if soup.find('script', src=lambda s: s and 'G-R7WY6BTL19' in s):
        return

    # Add GA snippet right after opening <head>
    ga_soup = BeautifulSoup(GA_SNIPPET, 'html.parser')
    
    if soup.head:
        soup.head.insert(0, ga_soup)
    else:
        print(f"No <head> found in {filepath}")

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    html_files = glob.glob('*.html')
    for file in html_files:
        print(f"Processing {file}...")
        process_file(file)
    print("Done!")
