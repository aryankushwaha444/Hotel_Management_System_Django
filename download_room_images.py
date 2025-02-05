import os
import requests
from urllib.parse import urlparse

# Sample room image URLs (replace with actual hotel room images)
room_images = {
    'single_room_101.jpg': 'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg',
    'double_room_102.jpg': 'https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg',
    'luxury_suite_201.jpg': 'https://images.pexels.com/photos/1457847/pexels-photo-1457847.jpeg',
    'double_room_202.jpg': 'https://images.pexels.com/photos/262048/pexels-photo-262048.jpeg',
    'executive_suite_301.jpg': 'https://images.pexels.com/photos/1743229/pexels-photo-1743229.jpeg'
}

def download_image(url, filename):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Create static/room_images directory if it doesn't exist
        os.makedirs('static/room_images', exist_ok=True)
        
        # Save the image
        file_path = os.path.join('static/room_images', filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
        
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

def main():
    print("Downloading room images...")
    for filename, url in room_images.items():
        download_image(url, filename)
    print("Done downloading images!")

if __name__ == '__main__':
    main()
