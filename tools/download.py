import os
import random
import time
import requests

START_INDEX = 107
MAX_IMAGES = 10

def main():
    # get random order for downloading images, except the indices already downloaded
    indices = random.sample(range(START_INDEX, START_INDEX + MAX_IMAGES), MAX_IMAGES)
    indices = [i for i in indices if not os.path.exists(f'download/img{i}.jpg')]  # Filter out already downloaded images
    for i in indices:
        # with exponential backoff in case of failure
        for attempt in range(5):
            try:
                download_img(i)
                break  # If download is successful, break out of the loop
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for image {i}: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
    time.sleep(random.uniform(0.5, 1.5))  # Sleep for a random time between 0.5 and 1.5 seconds to avoid overwhelming the server

def url(num: int):
    page_index_in_hex = hex(num)[2:].zfill(6).lower()
    link = f'https://dlcs.bl.digirati.io/iiif-img/v3/2/3/81055___vdc_100056065464.0x{page_index_in_hex}/full/2965,4096/0/default.jpg'
    print(f'Downloading image {num} from {link}')
    return link

def download_img(num: int):
    data = requests.get(url(num)).content
    f = open(f'download/img{num}.jpg','wb')
    f.write(data)
    f.close()

if __name__ == "__main__":
    main()
