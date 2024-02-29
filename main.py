
# # ----------------------------------------------------------------------------------------------------
# import os
# import shutil
# from keyword_extractor import extract_keywords
# from pygoogle_image import image as pi
# from image_classification import classify_images_for_solution
# import model as md
# from image_processor import process_and_classify_images
# # pip install pygoogle_image
# # pip install tensorflow  # Or tensorflow-gpu for GPU support
# # pip install keras       # If needed, though Keras is now integrated into TensorFlow
# # pip install Pillow      # For image processing
# # pip install opencv-python  # For OpenCV
# # pip install scikit-learn  
# # pip install pandas
# # pip install simple-image-download




# def main():
#     source_folder = "/homes/samatha94/ExAI/outputs/config_files"
#     destination_base_folder = "/homes/samatha94/ExAI/outputs/Google_images"
#     model_path = "/homes/samatha94/ExAI/outputs/model_resnet50V2_10classes_retest2023June.h5"
    
#     if not os.path.exists(destination_base_folder):
#         os.makedirs(destination_base_folder)
#         print("Google_images folder created successfully.")
#     else:
#         print("Google_images folder already exists.")

  


#     # Load the model
#     model, layer_outputs, layer_names, feature_map_model = md.load_and_analyze_model(model_path)
    
#     for i in range(2):
#         file_name = "neuron_{i}_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         solutions_keywords = extract_keywords(file_path)
#         print(solutions_keywords)

#         for solution, keywords in solutions_keywords.items():
#             combined_keywords = "_and_".join(keywords)  # Combine keywords for folder name
            
#             # Create the destination folder for each solution
#             neuron_solution_folder = os.path.join(destination_base_folder, 'neuron_{i}', solution)
#             os.makedirs(neuron_solution_folder, exist_ok=True)

#             # Adjust download call to use combined keywords
#             pi.download(keywords=combined_keywords, limit=10)  # Assuming this function can handle combined keyword searches

#             # Assuming downloaded images are saved in a default 'images' directory
#             downloaded_images_folder = os.path.join(os.getcwd(), 'images')
#             if os.path.exists(downloaded_images_folder):
#                 for filename in os.listdir(downloaded_images_folder):
#                     # Move images to the destination folder
#                     shutil.move(os.path.join(downloaded_images_folder, filename), neuron_solution_folder)
            
#             test_directory = neuron_solution_folder
#             new_classes = [combined_keywords]
#             process_and_classify_images(feature_map_model, test_directory, new_classes)

 
# if __name__ == "__main__":
#     main()
# ----------------------------------------------------------
# with selenium and beutiful soap  
import os
import shutil
from keyword_extractor import extract_keywords
from image_classification import classify_images_for_solution
import model as md
from image_processor import process_and_classify_images
import requests
from bs4 import BeautifulSoup

def download_images(search_query, dest_folder, num_images=100):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    downloaded_count = 0
    page = 0
    while downloaded_count < num_images:  # Continue until we've downloaded the desired number of images
        search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_query.replace(' ', '+')}&start={page * 100}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = [img['src'] for img in soup.find_all('img') if img.get('src') and not img['src'].startswith('data:image')]

        # If there are no more images found, break the loop
        if not images:
            print("No more images found.")
            break

        for img_url in images:
            if downloaded_count >= num_images:  # Break the inner loop if we've downloaded the desired number
                break
            try:
                img_data = requests.get(img_url).content
                img_filename = os.path.join(dest_folder, f"{search_query.replace(' ', '_')}_{downloaded_count + 1}.jpg")
                with open(img_filename, 'wb') as file:
                    file.write(img_data)
                downloaded_count += 1
            except Exception as e:
                print(f"Could not download image {img_url} - {e}")

        page += 1  # Go to the next page of search results

    print(f"Downloaded {downloaded_count} images for query '{search_query}'.")


def main():
    # source_folder = r"C:\Users\Dell-PC\OneDrive - Kansas State University\Desktop\DataSemantics prep\ExAI_2\outputs\config_files"
    # destination_base_folder = r"C:\Users\Dell-PC\OneDrive - Kansas State University\Desktop\DataSemantics prep\ExAI_2\outputs\Google_images"
    # model_path = r"C:\Users\Dell-PC\OneDrive - Kansas State University\Desktop\DataSemantics prep\ExAI_2\outputs\model_resnet50V2_10classes_retest2023June.h5"
    source_folder = "/homes/samatha94/ExAI/outputs/config_files"
    destination_base_folder = "/homes/samatha94/ExAI/outputs/Google_images"
    model_path = "/homes/samatha94/ExAI/outputs/model_resnet50V2_10classes_retest2023June.h5"
    if not os.path.exists(destination_base_folder):
        os.makedirs(destination_base_folder)
        print("Google_images folder created successfully.")
    else:
        print("Google_images folder already exists.")

    # Load the model
    model, layer_outputs, layer_names, feature_map_model = md.load_and_analyze_model(model_path)
    
   

    for i in range(2):
        file_name = f"neuron_{i}_results_ecii_V2.txt"  # Fixed string formatting
        file_path = os.path.join(source_folder, file_name)
        solutions_keywords = extract_keywords(file_path)
        print(solutions_keywords)

        for solution, keywords in solutions_keywords.items():
            combined_keywords = "_and_".join(keywords)  # Combine keywords for search query
            
            # Create the destination folder for each solution
            neuron_solution_folder = os.path.join(destination_base_folder, f'neuron_{i}', solution,combined_keywords)  # Fixed string formatting
            os.makedirs(neuron_solution_folder, exist_ok=True)        

            # Download images using simple-image-download
            download_images(combined_keywords, neuron_solution_folder, 10)

            # The simple_image_download saves images to a path based on the keyword in the script's directory.
            downloaded_images_folder = os.path.join(os.getcwd(), 'images')

            if os.path.exists(downloaded_images_folder):
                for filename in os.listdir(downloaded_images_folder):
                    # Move images to the destination folder
                    shutil.move(os.path.join(downloaded_images_folder, filename), neuron_solution_folder)
            
            test_directory = neuron_solution_folder
            new_classes = [combined_keywords]
            process_and_classify_images(feature_map_model, test_directory, new_classes)

if __name__ == "__main__":
    main()

# # ----------------------------------------------------------------------------------------------------
# API code-working
# import os
# from keyword_extractor import extract_keywords
# from image_downloader import download_images
# from image_classification import classify_images_for_solution
# from image_processor import process_and_evaluate_images
# import model as md

# def create_folder_structure(base_folder, neuron, solution, folder_name):
#     # neuron_folder = os.path.join(base_folder, f'neuron_{neuron}')
#     neuron_folder = os.path.join(base_folder, 'neuron_' + str(neuron))
#     solution_folder = os.path.join(neuron_folder, solution)
#     keyword_folder = os.path.join(solution_folder, folder_name.replace('_', ' '))
#     os.makedirs(keyword_folder, exist_ok=True)
#     return keyword_folder

# def main():
#     # source_folder = r"C:\Users\Dell-PC\OneDrive - Kansas State University\Desktop\DataSemantics prep\ExAI_2\outputs\config_files"
#     # destination_base_folder = r"C:\Users\Dell-PC\OneDrive - Kansas State University\Desktop\DataSemantics prep\ExAI_2\outputs\Google_images"
#     # model_path = r"C:\Users\Dell-PC\OneDrive - Kansas State University\Desktop\DataSemantics prep\ExAI_2\outputs\model_resnet50V2_10classes_retest2023June.h5"	
#     source_folder = "/homes/samatha94/ExAI/outputs/config_files"
#     destination_base_folder = "/homes/samatha94/ExAI/outputs/Google_images"
#     model_path = "/homes/samatha94/ExAI/outputs/model_resnet50V2_10classes_retest2023June.h5"
    
    
#     if not os.path.exists(destination_base_folder):
#         os.makedirs(destination_base_folder)
#         print("Google_images folder created successfully.")
#     else:
#         print("Google_images folder already exists.")

  


#     # Load the model
#     model, layer_outputs, layer_names, feature_map_model = md.load_and_analyze_model(model_path)
    
#     for i in range(2):  # For neuron indices 0 and 1
#         # file_name = f"neuron_{i}_results_ecii_V2.txt"
#         file_name = "neuron_" + str(i) + "_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         # print(file_path)
#         solutions_keywords = extract_keywords(file_path)
#         # print(solutions_keywords)

#         for solution, keywords in solutions_keywords.items():
#             # Combine keywords if there are multiple, else use as is
#             keyword_query = " and ".join(keywords)
#             print(keyword_query)
#             print("abc")
#             # Create a folder name based on combined keywords or single keyword
#             folder_name = " and ".join(keywords)
#             # download_images(keyword_query, destination_base_folder, i, solution, folder_name, limit=5)  # Adjust limit as needed
#             # download_images(keyword_query, destination_base_folder, i, solution, folder_name, limit=5)
            
#             # Create the folder structure and get the path
#             keyword_folder = create_folder_structure(destination_base_folder, i, solution, folder_name)
#             # Download images to the specific folder
#             download_images(keyword_query, keyword_folder,folder_name, limit=50)  # Adjust limit as needed
#             test_directory = keyword_folder
#             # new_classes = [keyword_query]
#             # process_and_classify_images(feature_map_model, test_directory, new_classes)
#             # Corrected call within main.py
#             process_and_evaluate_images(keyword_folder, feature_map_model, i, solution)


# if __name__ == "__main__":
#     main()
# -------------------------------------------------------------------------------------











































































