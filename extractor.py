import os
import requests
from bs4 import BeautifulSoup

def extract_manga(url, series_name, chapter_number):
    print(f"\n🚀 [Phase 1: EXTRACT] Starting Dedicated Scraper for {series_name} - Ch {chapter_number}")
    
    # 1. Create the workspace
    folder_name = f"{series_name}_{chapter_number}"
    os.makedirs(folder_name, exist_ok=True)
    
    # 2. Disguise our Python bot as a real Mac Safari browser
    # Unofficial pages block bots, with this we trick them.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    }

    try:
        print(f"🌐 Connecting to the website...")
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Stops everything if the link is down
        
        # 3. Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Find all image tags (<img>)
        images = soup.find_all('img')
        
        counter = 1
        print(f"🔍 DIAGNOSTIC: The page returned {len(images)} <img> tags in total.")
        print("📥 Downloading and sorting pages...")
        
        for img in images:
            # 1. Detective Mode: Print ALL image attributes to see where they hide the real link
            print(f"\n🔍 Analyzing attributes: {img.attrs}")
            
            # 2. Reverse priority: First we look in the 'data' attributes, and LAST in the normal 'src'.
            img_link = img.get('data-src') or img.get('data-lazy-src') or img.get('data-original') or img.get('src')
            
            # 3. If unfortunately we grab the phantom SVG, we skip it manually
            if img_link and img_link.startswith('data:image'):
                print("   ⚠️ Base64 placeholder detected. Ignoring...")
                continue
                
            # Fix the filter so it's bulletproof
            if img_link and any(ext in img_link.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
                
                print(f"   🎯 Real link found: {img_link}")
                # Download the bytes of the image
                img_data = requests.get(img_link, headers=headers).content
                
                # Extract the extension (.jpg, .webp) and apply zero-padding (001, 002)
                extension = img_link.split('.')[-1]
                file_name = f"{counter:03d}.{extension}"
                file_path = os.path.join(folder_name, file_name)
                
                # Save the file to the hard drive
                with open(file_path, 'wb') as local_file:
                    local_file.write(img_data)
                    
                print(f"   ✔️ Saved: {file_name}")
                counter += 1
        
        print(f"✅ Mission accomplished! {counter - 1} pages saved in: {folder_name}")
        return folder_name

    except Exception as error:
        print(f"❌ Scraper Error: {error}")
        return None

# --- Test Block ---
if __name__ == '__main__':
    url_input = input("Enter the manga chapter URL: ")
    series_name_input = input("Enter the series name (e.g., Blue_Lock): ")
    chapter_number_input = input("Enter the chapter number (e.g., 016): ")
    
    extract_manga(url_input, series_name_input, chapter_number_input)