import os
import glob
from bs4 import BeautifulSoup

def inject_language_switcher():
    # Process root (EN) and zh-cn, zh-tw
    for root_dir in ['.', 'zh-cn', 'zh-tw']:
        for filepath in glob.glob(os.path.join(root_dir, '*.html')):
            basename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Find the navbar container
            nav = soup.find('nav')
            if not nav:
                print(f"Skipping {filepath} - no nav tag found.")
                continue

            # We check if language switcher is already there
            if nav.find(id='language-switcher'):
                print(f"Skipping {filepath} - language switcher already exists.")
                continue
                
            # Find the div that contains "Make an Appointment" (or whatever the localized string is)
            # It's inside a <div class="flex-shrink-0"> inside nav > div.max-w-7xl
            button_container = None
            
            # The logo is also flex-shrink-0, but it contains an img, the button contains an `a` with class bg-brand-olive
            for div in nav.find_all('div', class_='flex-shrink-0'):
                a_tag = div.find('a', class_=lambda c: c and 'bg-brand-olive' in c)
                if a_tag:
                    button_container = div
                    break
            
            if button_container:
                # Based on the user's directory depth, we construct the relative links for the switcher
                # If we are in `zh-cn/home.html`, the links should be:
                # EN -> ../home.html
                # 简 -> home.html
                # 繁 -> ../zh-tw/home.html
                # To be absolutely robust, we can just use root-relative paths like `/home.html` and let Netlify serve it.
                # However, for local file testing, relative paths are safer.
                if root_dir == '.':
                    en_link = f"{basename}"
                    cn_link = f"zh-cn/{basename}"
                    tw_link = f"zh-tw/{basename}"
                elif root_dir == 'zh-cn':
                    en_link = f"../{basename}"
                    cn_link = f"{basename}"
                    tw_link = f"../zh-tw/{basename}"
                elif root_dir == 'zh-tw':
                    en_link = f"../{basename}"
                    cn_link = f"../zh-cn/{basename}"
                    tw_link = f"{basename}"

                switcher_html = f"""
                <div id="language-switcher" class="flex items-center space-x-2 text-xs font-bold tracking-widest text-brand-deep/80 mr-4 md:mr-6">
                  <a href="{en_link}" class="hover:text-brand-olive transition-colors">EN</a>
                  <span class="text-brand-olive/30">|</span>
                  <a href="{cn_link}" class="hover:text-brand-olive transition-colors font-sans">简</a>
                  <span class="text-brand-olive/30">|</span>
                  <a href="{tw_link}" class="hover:text-brand-olive transition-colors font-sans">繁</a>
                </div>
                """
                
                switcher_soup = BeautifulSoup(switcher_html, 'html.parser')
                
                # Wrap the switcher and button in a flex div 
                wrapper = soup.new_tag('div')
                wrapper['class'] = 'flex items-center'
                
                button_container.insert_before(wrapper)
                wrapper.append(switcher_soup)
                wrapper.append(button_container.extract())
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"Injected into {filepath}")

if __name__ == '__main__':
    inject_language_switcher()
    print("Done!")
