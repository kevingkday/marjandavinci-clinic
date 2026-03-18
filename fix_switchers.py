import os
import glob
from bs4 import BeautifulSoup

def fix_switchers():
    for root_dir in ['.', 'zh-cn', 'zh-tw']:
        for filepath in glob.glob(os.path.join(root_dir, '*.html')):
            basename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Find old switcher and remove it
            old_switcher = soup.find(id='language-switcher')
            if old_switcher:
                old_switcher.decompose()
            
            nav = soup.find('nav')
            if not nav: continue
            
            button_container = None
            for div in nav.find_all('div', class_='flex-shrink-0'):
                a_tag = div.find('a', class_=lambda c: c and 'bg-brand-olive' in c)
                if a_tag:
                    button_container = div
                    break
            
            if button_container:
                en_link = f"/{basename}"
                cn_link = f"/zh-cn/{basename}"
                tw_link = f"/zh-tw/{basename}"

                switcher_html = f"""
                <div id="language-switcher" class="flex items-center space-x-3 text-sm font-bold tracking-widest text-brand-deep/80 mr-4 md:mr-6" translate="no">
                  <a href="{en_link}" class="hover:text-brand-olive transition-colors font-sans">EN</a>
                  <span class="text-brand-olive/30">|</span>
                  <a href="{cn_link}" class="hover:text-brand-olive transition-colors font-sans">简</a>
                  <span class="text-brand-olive/30">|</span>
                  <a href="{tw_link}" class="hover:text-brand-olive transition-colors font-sans">繁</a>
                </div>
                """
                
                switcher_soup = BeautifulSoup(switcher_html, 'html.parser')
                
                # Check if it's already inside a wrapper 
                # (the layout fix from earlier generated <div class="flex items-center">)
                parent = button_container.parent
                if 'flex' in parent.get('class', []) and 'items-center' in parent.get('class', []) and parent.name == 'div':
                    button_container.insert_before(switcher_soup)
                else:
                    # If for some reason it's not wrapped
                    wrapper = soup.new_tag('div')
                    wrapper['class'] = 'flex items-center'
                    button_container.insert_before(wrapper)
                    wrapper.append(switcher_soup)
                    wrapper.append(button_container.extract())
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
            
if __name__ == '__main__':
    fix_switchers()
    print("Fixed Language Switchers.")
