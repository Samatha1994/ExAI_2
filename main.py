
# # ----------------------------------------------------------------------------------------------------
import os
import shutil
from keyword_extractor import extract_keywords
from pygoogle_image import image as pi
from image_classification import classify_images_for_solution
import model as md
from image_processor import process_and_classify_images
# pip install pygoogle_image
# pip install tensorflow  # Or tensorflow-gpu for GPU support
# pip install keras       # If needed, though Keras is now integrated into TensorFlow
# pip install Pillow      # For image processing
# pip install opencv-python  # For OpenCV
# pip install scikit-learn  
# pip install pandas



def main():
    source_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\config_files"
    destination_base_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\Google_images"
    model_path = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\model_resnet50V2_10classes_retest2023June.h5"
    # Use the WORKSPACE environment variable to get the root directory of the Jenkins workspace
    workspace_path = os.getenv('WORKSPACE', '')

    # Construct paths relative to the Jenkins workspace
    # source_folder = os.path.join(workspace_path, 'outputs', 'config_files')
    # destination_base_folder = os.path.join(workspace_path, 'outputs', 'Google_images')
    # model_path = os.path.join(workspace_path, 'outputs', 'model_resnet50V2_10classes_retest2023June.h5')

    # Check if the Google_images folder exists and create it if it doesn't
    if not os.path.exists(destination_base_folder):
        os.makedirs(destination_base_folder)
        print(f"'{destination_base_folder}' created successfully.")
    else:
        print(f"'{destination_base_folder}' already exists.")

  


    # Load the model
    model, layer_outputs, layer_names, feature_map_model = md.load_and_analyze_model(model_path)
    
    for i in range(2):
        file_name = f"neuron_{i}_results_ecii_V2.txt"
        file_path = os.path.join(source_folder, file_name)
        solutions_keywords = extract_keywords(file_path)
        print(solutions_keywords)

        for solution, keywords in solutions_keywords.items():
            combined_keywords = "_and_".join(keywords)  # Combine keywords for folder name
            
            # Create the destination folder for each solution
            neuron_solution_folder = os.path.join(destination_base_folder, f'neuron_{i}', solution)
            os.makedirs(neuron_solution_folder, exist_ok=True)

            # Adjust download call to use combined keywords
            pi.download(keywords=combined_keywords, limit=10)  # Assuming this function can handle combined keyword searches

            # Assuming downloaded images are saved in a default 'images' directory
            downloaded_images_folder = os.path.join(os.getcwd(), 'images')
            if os.path.exists(downloaded_images_folder):
                for filename in os.listdir(downloaded_images_folder):
                    # Move images to the destination folder
                    shutil.move(os.path.join(downloaded_images_folder, filename), neuron_solution_folder)
            # --------------------------------------------------------------------------------------------------------
            # old code for Batch images section
            # Classification (assuming this part remains unchanged)
            # new_classes = keywords  # This may need adjustment based on how classification is handled
            # classify_images_for_solution(solution, neuron_solution_folder, model_path, new_classes, i)      
            # --------------------------------------------------------------------------------------------------------    
            
            # new_classes = [combined_keywords.replace('_and_', ' and ') for combined_keywords in new_classes]
             
            test_directory = neuron_solution_folder
            new_classes = [combined_keywords]
            process_and_classify_images(feature_map_model, test_directory, new_classes)

        



if __name__ == "__main__":
    main()
# # ----------------------------------------------------------------------------------------------------
# import os
# from keyword_extractor import extract_keywords
# from image_downloader import download_images

# def main():
#     source_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\config_files"
#     destination_base_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\Google_images"

#     for i in range(2):  # For neuron indices 0 and 1
#         file_name = f"neuron_{i}_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         solutions_keywords = extract_keywords(file_path)
#         print(solutions_keywords)

#         for solution, keywords in solutions_keywords.items():
#             # Combine keywords if there are multiple, else use as is
#             keyword_query = " and ".join(keywords)
#             # Create a folder name based on combined keywords or single keyword
#             folder_name = " and ".join(keywords)
#             download_images(keyword_query, destination_base_folder, i, solution, folder_name, limit=10)  # Adjust limit as needed

# if __name__ == "__main__":
#     main()

# import os
# import shutil
# from keyword_extractor import extract_keywords
# # import pygoogle_image as pi
# from pygoogle_image import image as pi
# from image_processor import process_and_classify_images
# import model as md

# def main():
#     workspace_path = os.getenv('WORKSPACE', '')
#     source_folder = os.path.join(workspace_path, 'outputs', 'config_files')
#     destination_base_folder = os.path.join(workspace_path, 'outputs', 'Google_images')
#     model_path = os.path.join(workspace_path, 'outputs', 'model_resnet50V2_10classes_retest2023June.h5')

#     if not os.path.exists(destination_base_folder):
#         os.makedirs(destination_base_folder)
#         print(f"'{destination_base_folder}' created successfully.")
#     else:
#         print(f"'{destination_base_folder}' already exists.")

#     model, layer_outputs, layer_names, feature_map_model = md.load_and_analyze_model(model_path)

#     for i in range(2):
#         file_name = f"neuron_{i}_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         solutions_keywords = extract_keywords(file_path)

#         for solution, keywords in solutions_keywords.items():
#             combined_keywords = "_and_".join(set(keywords))  # Ensure unique keywords only
#             keyword_folder = os.path.join(destination_base_folder, f'neuron_{i}', combined_keywords)
#             os.makedirs(keyword_folder, exist_ok=True)

#             # Download images using combined keywords. 
#             # This assumes images are downloaded to a default 'images' folder. Adjust as necessary.
#             pi.download(keywords=combined_keywords, limit=200)
            
#             # Move downloaded images to the desired folder
#             # Assumes images are downloaded to a default directory that needs to be specified
#             default_download_folder = os.path.join(os.getcwd(), 'images')  # Adjust this path as necessary
#             if os.path.exists(default_download_folder):
#                 for filename in os.listdir(default_download_folder):
#                     shutil.move(os.path.join(default_download_folder, filename), keyword_folder)

#             # Process and classify images
#             new_classes = [combined_keywords]
#             process_and_classify_images(feature_map_model, keyword_folder, new_classes)

# if __name__ == "__main__":
#     main()
# -----------------------------------------------------------------------------------------------

# import os
# import shutil
# from keyword_extractor import extract_keywords
# from google_images_download import google_images_download
# from image_processor import process_and_classify_images
# import model as md

# def download_images(keywords, limit, dest_folder):
#     response = google_images_download.googleimagesdownload()
#     arguments = {"keywords": keywords, "limit": limit, "print_urls": True, "output_directory": dest_folder}
#     paths = response.download(arguments)
#     print(paths)

# def main():
#     workspace_path = os.getenv('WORKSPACE', '')
#     source_folder = os.path.join(workspace_path, 'outputs', 'config_files')
#     destination_base_folder = os.path.join(workspace_path, 'outputs', 'Google_images')
#     model_path = os.path.join(workspace_path, 'outputs', 'model_resnet50V2_10classes_retest2023June.h5')

#     if not os.path.exists(destination_base_folder):
#         os.makedirs(destination_base_folder)
#         print(f"'{destination_base_folder}' created successfully.")
#     else:
#         print(f"'{destination_base_folder}' already exists.")

#     model, layer_outputs, layer_names, feature_map_model = md.load_and_analyze_model(model_path)

#     for i in range(2):
#         file_name = f"neuron_{i}_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         solutions_keywords = extract_keywords(file_path)

#         for solution, keywords in solutions_keywords.items():
#             combined_keywords = "_and_".join(set(keywords))  # Ensure unique keywords only
#             keyword_folder = os.path.join(destination_base_folder, f'neuron_{i}', combined_keywords)
#             os.makedirs(keyword_folder, exist_ok=True)

#             # Download images using combined keywords
#             download_images(keywords=combined_keywords, limit=200, dest_folder=keyword_folder)
            
#             # Process and classify images
#             new_classes = [combined_keywords]
#             process_and_classify_images(feature_map_model, keyword_folder, new_classes)

# if __name__ == "__main__":
#     main()








































































# -------------------------------------------------------------------
# API CODE:
# import os
# from keyword_extractor import extract_keywords
# # from image_downloader import download_images
# from downloaders.google_downloader import download_images_from_google
# from downloaders.pixabay_downloader import download_images_from_pixabay
# from downloaders.unsplash_downloader import download_images_from_unsplash
# from downloaders.pexels_downloader import download_images_from_pexels


# def main():
#     source_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\config_files"
#     destination_base_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\Google_images"

#     for i in range(2):  # For neuron indices 0 and 1
#         file_name = f"neuron_{i}_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         solutions_keywords = extract_keywords(file_path)
#         print(solutions_keywords)

#         for solution, keywords in solutions_keywords.items():
#             # Combine keywords if there are multiple, else use as is
#             keyword_query = " and ".join(keywords)
#             # Create a folder name based on combined keywords or single keyword
#             folder_name = " and ".join(keywords)
#             # download_images(keyword_query, destination_base_folder, i, solution, folder_name, limit=200)  # Adjust limit as needed

#             download_images_from_google(keyword_query, destination_base_folder, i, solution, folder_name, limit=50)
#             download_images_from_pixabay(keyword_query, destination_base_folder, i, solution, folder_name, limit=50)
#             download_images_from_unsplash(keyword_query, destination_base_folder, i, solution, folder_name, limit=50)
#             download_images_from_pexels(keyword_query, destination_base_folder, i, solution, folder_name, limit=50)

# if __name__ == "__main__":
#     main()
# -------------------------------------------------------------------
# import os
# from keyword_extractor import extract_keywords
# from downloaders.google_downloader import download_images_from_google
# from downloaders.pixabay_downloader import download_images_from_pixabay
# from downloaders.unsplash_downloader import download_images_from_unsplash
# from downloaders.pexels_downloader import download_images_from_pexels

# def download_images_adjusted(keyword, destination_base_folder, neuron_index, solution_name, folder_name, total_limit=200):
#     total_downloaded = 0
#     downloaders = [
#         (download_images_from_google, "Google"),
#         # (download_images_from_pixabay, "Pixabay"),
#         # (download_images_from_unsplash, "Unsplash"),
#         (download_images_from_pexels, "Pexels"),
#     ]

#     # Modify folder name to remove spaces and concatenate with an underscore for the image filename.
#     folder_name = folder_name.replace(" and ", "_").replace(" ", "_")

#     for downloader, name in downloaders:
#         if total_downloaded < total_limit:
#             remaining_limit = total_limit - total_downloaded
#             try:
#                 downloaded = downloader(keyword, destination_base_folder, neuron_index, solution_name, folder_name, limit=remaining_limit, start_number=total_downloaded)
#                 total_downloaded += downloaded
#                 print(f"{name} downloader downloaded {downloaded} images for '{keyword}'. Total downloaded: {total_downloaded}.")
#             except Exception as e:
#                 print(f"Error with {name} downloader for '{keyword}': {e}")
#         else:
#             break

#     print(f"Total images downloaded for '{keyword}': {total_downloaded}")

# def main():
#     source_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\config_files"
#     destination_base_folder = r"C:\ProgramData\Jenkins\.jenkins\workspace\ExAI_ECII_BOTH\outputs\Google_images"

#     for i in range(2):  # For neuron indices 0 and 1
#         file_name = f"neuron_{i}_results_ecii_V2.txt"
#         file_path = os.path.join(source_folder, file_name)
#         solutions_keywords = extract_keywords(file_path)
#         print(solutions_keywords)

#         for solution, keywords in solutions_keywords.items():
#             keyword_query = " ".join(keywords)  # Removed "and" for better search results.
#             folder_name = "_".join(keywords)  # Use underscores for folder names.
#             download_images_adjusted(keyword_query, destination_base_folder, i, solution, folder_name, total_limit=200)

# if __name__ == "__main__":
#     main()



