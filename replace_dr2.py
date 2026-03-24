import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace variations of Dr. Sahih (Injectables):
    # For English:
    content = re.sub(r'Call Dr\. Sahih \(Injectables\):\s*', 'Call ', content)
    content = re.sub(r'Dr\. Sahih \(Injectables\):\s*778-707-4377', 'Call 778-707-4377', content)
    content = re.sub(r'Dr\. Sahih \(Injectables\):\s*', 'Call: ', content)
    
    # For zh-cn (Simplified)
    content = re.sub(r'致电 Sahih 医生?[（\(]注射剂?[）\)]：\s*', '致电：', content)
    content = re.sub(r'博士。? Sahih[（\(]注射剂?[）\)]：\s*778-707-4377', '致电 778-707-4377', content)
    content = re.sub(r'博士。? Sahih[（\(]注射剂?[）\)]：\s*', '致电：', content)

    # For zh-tw (Traditional)
    content = re.sub(r'請?致電 Sahih 醫[生師][（\(]注射劑?[）\)]：\s*', '致電 ', content)
    content = re.sub(r'Sahih 博士[（\(]注射劑?[）\)]：\s*778-707-4377', '致電 778-707-4377', content)
    content = re.sub(r'Sahih 博士[（\(]注射劑?[）\)]：\s*', '致電：', content)
    content = re.sub(r'博士。? Sahih[（\(]注射劑?[）\)]：\s*778-707-4377', '致電 778-707-4377', content)
    content = re.sub(r'博士。? Sahih[（\(]注射劑?[）\)]：\s*', '致電：', content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")

base_dir = r"d:\GitHub\marjandavinci.com"
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith('.html'):
            process_file(os.path.join(root, name))

print("Regex replacement complete.")
