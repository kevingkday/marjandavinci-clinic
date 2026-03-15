import os
import glob
from bs4 import BeautifulSoup
import json

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # Check if meta tags already exist to avoid duplication
    if soup.find('meta', {'name': 'description'}):
        return

    title = soup.title.string if soup.title else "Marjan DaVinci Laser & Cosmetic"
    
    # 1. Add Meta Description
    meta_desc = soup.new_tag('meta', attrs={'name': 'description', 'content': f"{title} in Richmond, BC. Discover premium medical aesthetic treatments including Botox, fillers, laser hair removal, and skin rejuvenation at Marjan DaVinci."})
    soup.head.append(meta_desc)
    soup.head.append("\n  ")

    # 2. Add Open Graph Tags
    og_title = soup.new_tag('meta', attrs={'property': 'og:title', 'content': title})
    og_desc = soup.new_tag('meta', attrs={'property': 'og:description', 'content': meta_desc['content']})
    og_image = soup.new_tag('meta', attrs={'property': 'og:image', 'content': 'https://assets.cdn.filesafe.space/pWlFe9i46QOOHhVfmtgR/media/69b181d278565a0df93b77ce.png'})
    og_type = soup.new_tag('meta', attrs={'property': 'og:type', 'content': 'website'})
    
    soup.head.append(og_title)
    soup.head.append("\n  ")
    soup.head.append(og_desc)
    soup.head.append("\n  ")
    soup.head.append(og_image)
    soup.head.append("\n  ")
    soup.head.append(og_type)
    soup.head.append("\n  ")

    # 3. Add Local Business Schema (JSON-LD)
    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": "Marjan DaVinci Laser & Cosmetic",
        "image": "https://assets.cdn.filesafe.space/pWlFe9i46QOOHhVfmtgR/media/69b181d278565a0df93b77ce.png",
        "@id": "https://marjandavinci.com",
        "url": "https://marjandavinci.com",
        "telephone": "+17789992416",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "6388 No. 3 Rd, 11th Floor, Suite 1110",
            "addressLocality": "Richmond",
            "addressRegion": "BC",
            "postalCode": "V6Y 2B3",
            "addressCountry": "CA"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 49.1666824,
            "longitude": -123.135496
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ],
            "opens": "09:00",
            "closes": "17:00"
        },
        "priceRange": "$$"
    }
    
    schema_script = soup.new_tag('script', type='application/ld+json')
    schema_script.string = json.dumps(schema, indent=2)
    soup.head.append(schema_script)
    soup.head.append("\n")

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    html_files = glob.glob('*.html')
    for file in html_files:
        print(f"Processing {file}...")
        process_file(file)
    print("Done!")
