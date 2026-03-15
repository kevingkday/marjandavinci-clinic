import glob

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        data = file.read()
    
    changed = False
    
    target_cta = 'Call Dr. Sahih (Injectables): 778-707-4377'
    replacement_cta = 'Call Dr. Sahih (Injectables): <span class="whitespace-nowrap">778-707-4377</span>'
    if target_cta in data:
        data = data.replace(target_cta, replacement_cta)
        changed = True

    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(data)
        print('Updated ' + f)
