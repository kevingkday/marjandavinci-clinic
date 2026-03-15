import glob

script_to_add = """<script 
  src="https://widgets.leadconnectorhq.com/loader.js"  
  data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" 
  data-widget-id="69863e437cd1e63a788d2e56"   > 
</script>
</body>"""

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Check if script is already present to prevent duplicates just in case
    if 'data-widget-id="69863e437cd1e63a788d2e56"' not in data:
        data = data.replace('</body>', script_to_add)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(data)
        print('Added chat widget to ' + f)
