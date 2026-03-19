import os
import glob

def rename_and_update():
    # 1. Rename files
    for root_dir in ['.', 'zh-cn', 'zh-tw']:
        old_path = os.path.join(root_dir, 'home.html')
        new_path = os.path.join(root_dir, 'index.html')
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    # 2. Update references in all HTML files
    for root_dir in ['.', 'zh-cn', 'zh-tw']:
        for filepath in glob.glob(os.path.join(root_dir, '*.html')):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            new_content = content.replace('href="home.html"', 'href="index.html"')
            new_content = new_content.replace('href="/home.html"', 'href="/"')
            new_content = new_content.replace('href="../home.html"', 'href="../index.html"')
            new_content = new_content.replace('href="/zh-cn/home.html"', 'href="/zh-cn/"')
            new_content = new_content.replace('href="/zh-tw/home.html"', 'href="/zh-tw/"')
            new_content = new_content.replace('href="zh-cn/home.html"', 'href="zh-cn/"')
            new_content = new_content.replace('href="zh-tw/home.html"', 'href="zh-tw/"')

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
    # 3. Update XML/TXT files
    for meta_file in ['sitemap.xml', 'robots.txt', 'netlify.toml']:
        if os.path.exists(meta_file):
            with open(meta_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            new_content = content.replace('home.html', 'index.html')
            
            if new_content != content:
                with open(meta_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == '__main__':
    rename_and_update()
    print("Renamed home.html to index.html and updated all links.")
