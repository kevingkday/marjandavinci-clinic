import glob

old_map_url = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d115681.29592733351!2d-122.477646!3d37.7277583!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8090f4886e7a5ba7%3A0x7e7c9f6927a42b1d!2s6388%20No.%203%20Rd%2011th%20Floor%2C%20Suite%201110%2C%20Richmond%2C%20BC%20V6Y%200L4%2C%20Canada!5e0!3m2!1sen!2sus!4v1709400000000!5m2!1sen!2sus&cid=9112691923326036573'
new_map_url = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3094.53574709007!2d-123.135496!3d49.1666824!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x548675262bb08ead%3A0x7e76c905ed6b6a5d!2sMarjan%20DaVinci%20Laser%20%26%20Cosmetic%20Clinic!5e1!3m2!1sen!2sca!4v1773448067594!5m2!1sen!2sca" referrerpolicy="no-referrer-when-downgrade'

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        data = file.read()
    
    if old_map_url in data:
        data = data.replace(old_map_url, new_map_url)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(data)
        print('Updated map in ' + f)
