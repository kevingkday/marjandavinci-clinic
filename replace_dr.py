import os
import glob

# Replace mappings
replacements = {
    # English
    'Dr. Sahih (Injectables): 778-707-4377': 'Call 778-707-4377',
    'Call Dr. Sahih (Injectables):': 'Call:',
    'Dr. Sahih (Injectables):': 'Call:',
    # zh-cn
    '博士。 Sahih（注射剂）：778-707-4377': '致电 778-707-4377',
    '致电 Sahih 医生（注射剂）：': '致电：',
    '致电 Sahih 医生（注射）：': '致电：',
    'Sahih 博士（注射剂）：': '致电：',
    # zh-tw
    'Sahih 博士（注射劑）：778-707-4377': '致電 778-707-4377',
    '致電 Sahih 醫生（注射劑）：': '致電：',
    '致電 Sahih 醫生（注射）：': '致電：',
    'Sahih 博士（注射劑）：': '致電：',
    '博士。 Sahih（注射劑）：778-707-4377': '致電 778-707-4377',
}

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")

# Find all HTML files recursively
base_dir = r"d:\GitHub\marjandavinci.com"
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if name.endswith('.html'):
            process_file(os.path.join(root, name))

print("Replacement complete.")
