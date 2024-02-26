# import os
# import requests
# import shutil
# from urllib.parse import urlparse

# # Replace with your actual API keys and Custom Search Engine ID
# GOOGLE_API_KEY = 'AIzaSyDqlNYYlxReH51VNgvCFCzfkihxhBU0uEs'
# CSE_ID = '933de8d069a4a4c8e'
# PIXABAY_API_KEY = '42268427-0a13229ada64525c7727bef88'

# def sanitize_filename(url):
#     parsed_url = urlparse(url)
#     filename = os.path.basename(parsed_url.path)
#     invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
#     for char in invalid_chars:
#         filename = filename.replace(char, '_')
#     return filename

# def create_folder_structure(base_folder, neuron, solution, folder_name):
#     neuron_folder = os.path.join(base_folder, f'neuron_{neuron}')
#     solution_folder = os.path.join(neuron_folder, solution)
#     keyword_folder = os.path.join(solution_folder, folder_name.replace('_', ' '))
#     os.makedirs(keyword_folder, exist_ok=True)
#     return keyword_folder

# def download_image(image_url, folder_name, keyword_folder, image_number):
#     try:
#         img_response = requests.get(image_url, stream=True)
#         if img_response.status_code == 200:
#             image_name = f"{folder_name}_{image_number}.jpg"
#             file_path = os.path.join(keyword_folder, image_name)
#             with open(file_path, 'wb') as f:
#                 img_response.raw.decode_content = True
#                 shutil.copyfileobj(img_response.raw, f)
#             return True
#     except Exception as e:
#         print(f"Failed to download {image_url}. Reason: {e}")
#     return False

# def download_images_from_google(keyword, keyword_folder, folder_name, images_downloaded, limit):
#     google_search_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         'q': keyword,
#         'cx': CSE_ID,
#         'key': GOOGLE_API_KEY,
#         'searchType': 'image',
#         'num': 10,
#         'fileType': 'jpg|png',
#     }
#     while images_downloaded < limit:
#         params['start'] = images_downloaded + 1
#         response = requests.get(google_search_url, params=params).json()
#         if 'items' not in response:
#             break
#         for item in response['items']:
#             if download_image(item['link'], folder_name, keyword_folder, images_downloaded + 1):
#                 images_downloaded += 1
#             if images_downloaded >= limit:
#                 return images_downloaded
#     return images_downloaded

# def download_images_from_pixabay(keyword, keyword_folder, folder_name, images_downloaded, limit):
#     params = {
#         "key": PIXABAY_API_KEY,
#         "q": keyword,
#         "image_type": "photo",
#         "per_page": 200,
#     }
#     response = requests.get("https://pixabay.com/api/", params=params).json()
#     if 'hits' not in response:
#         return images_downloaded
#     for item in response['hits']:
#         if download_image(item['webformatURL'], folder_name, keyword_folder, images_downloaded + 1):
#             images_downloaded += 1
#         if images_downloaded >= limit:
#             break
#     return images_downloaded

# def download_images(keyword, base_folder, neuron_index, solution_name, folder_name, limit=200):
#     keyword_folder = create_folder_structure(base_folder, neuron_index, solution_name, folder_name)
#     images_downloaded = 0
#     images_downloaded = download_images_from_google(keyword, keyword_folder, folder_name, images_downloaded, limit)
#     if images_downloaded < limit:
#         images_downloaded = download_images_from_pixabay(keyword, keyword_folder, folder_name, images_downloaded, limit)
#     print(f"Total images downloaded for {keyword}: {images_downloaded}")

import os
import requests
import shutil
from urllib.parse import urlparse

def sanitize_filename(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# def create_folder_structure(base_folder, neuron, solution, folder_name):
#     neuron_folder = os.path.join(base_folder, f'neuron_{neuron}')
#     solution_folder = os.path.join(neuron_folder, solution)
#     keyword_folder = os.path.join(solution_folder, folder_name.replace('_', ' '))
#     os.makedirs(keyword_folder, exist_ok=True)
#     return keyword_folder

def download_images(keyword, keyword_folder,folder_name, limit=50, api_key="AIzaSyDqlNYYlxReH51VNgvCFCzfkihxhBU0uEs", cse_id="933de8d069a4a4c8e"):
# def download_images(keyword, base_folder, neuron_index, solution_name, folder_name, limit=5, api_key="AIzaSyDqlNYYlxReH51VNgvCFCzfkihxhBU0uEs", cse_id="933de8d069a4a4c8e"):
    # keyword_folder = create_folder_structure(base_folder, neuron_index, solution_name, folder_name)
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': keyword,
        'cx': cse_id,
        'key': api_key,
        'searchType': 'image',
        'num': 10,  # Adjust if you need more per request, up to 10
        'fileType': 'jpg|png',
    }
    images_downloaded = 0
    start_index = 1
    while images_downloaded < limit:
        params['start'] = start_index
        response = requests.get(search_url, params=params).json()
        if 'items' not in response:
            print("No more images found or there's an error.")
            break
        for item in response['items']:
            image_url = item['link']
            try:
                img_response = requests.get(image_url, stream=True)
                if img_response.status_code == 200:
                    # Naming images sequentially according to the specification
                    # image_name = f"{folder_name} {images_downloaded + 1}.jpg"
                    image_name = folder_name + " " + str(images_downloaded + 1) + ".jpg"
                    file_path = os.path.join(keyword_folder, image_name)
                    with open(file_path, 'wb') as f:
                        img_response.raw.decode_content = True
                        shutil.copyfileobj(img_response.raw, f)
                    images_downloaded += 1
                    if images_downloaded >= limit:
                        break
            except Exception as e:
                # print(f"Failed to download {image_url}. Reason: {e}")
                print("Failed to download " + image_url + ". Reason: " + str(e))
        start_index += 10





