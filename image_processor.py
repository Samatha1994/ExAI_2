import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing import image
from sklearn.model_selection import train_test_split

def process_and_classify_images(feature_map_model, test_directory, new_classes):

    # new_classes = [class_name.replace('_and_', ' and ') for class_name in new_classes]
    print(new_classes)
    # Create an ImageDataGenerator for rescaling
    rescale_generator = image.ImageDataGenerator(rescale=1./255)

    # Load the test images for the new classes
    test_images = []
    filenames = []
    class_names = []
    print(new_classes)
    # Loop through each class directory and load images
    for class_name in new_classes:

        class_directory = os.path.join(test_directory, class_name)  
        for image_name in os.listdir(class_directory):
            image_path = os.path.join(class_directory, image_name)
            img = image.load_img(image_path, target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = rescale_generator.standardize(img)
            test_images.append(img)
            filenames.append(image_name)
            class_names.append(class_name)

    print(class_name)
    # Concatenate the test images into a single array
    test_images = np.concatenate(test_images)
    print(class_names)
    # Split the data into training and validation sets
    train_images, val_images, train_filenames, val_filenames, train_class_names, val_class_names = train_test_split(
        test_images, filenames, class_names, test_size=0.2, random_state=42)

    # Perform predictions for the new training images
    train_predIdxs = feature_map_model.predict(train_images)
    train_classes = list(np.argmax(train_predIdxs, axis=1))

    # Perform predictions for the new validation images
    val_predIdxs = feature_map_model.predict(val_images)
    val_classes = list(np.argmax(val_predIdxs, axis=1))

    # Create dataframes for training and validation sets
    train_df = pd.DataFrame(train_predIdxs)
    train_df['Class_names'] = train_class_names
    train_df['Filenames'] = train_filenames
    train_df['Predicted_classes'] = train_classes

    val_df = pd.DataFrame(val_predIdxs)
    val_df['Class_names'] = val_class_names
    val_df['Filenames'] = val_filenames
    val_df['Predicted_classes'] = val_classes

    # Save the dataframes to CSV files in the parent folder of the solution directories
    for class_name in new_classes:
        solution_name = class_name.split(' and ')[0]  # Extract the solution name
        solution_directory = os.path.join(test_directory, class_name)
        parent_directory = os.path.dirname(solution_directory)
        os.makedirs(parent_directory, exist_ok=True)

        eval_csv_path = os.path.join(parent_directory, f'{solution_name}_evaluation_set.csv')
        verif_csv_path = os.path.join(parent_directory, f'{solution_name}_verification_set.csv')

        train_df[train_df['Class_names'] == class_name].to_csv(eval_csv_path, index=None, header=True)
        val_df[val_df['Class_names'] == class_name].to_csv(verif_csv_path, index=None, header=True)

