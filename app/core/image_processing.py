import numpy as np
import requests
from PIL import Image
import tensorflow as tf

def get_image_category(predictions, class_labels):
    """
    Determine the category of an image based on its predictions.

    Args:
    - predictions (numpy array): Model prediction probabilities.
    - class_labels (list): List of class labels in the same order as the model's output.

    Returns:
    - str: The category of the image.
    """
    # Check if predictions have valid shape
    if predictions.ndim != 2 or predictions.shape[0] != 1:
        raise ValueError("Predictions should have shape (1, num_classes)")

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_labels[predicted_class_index]

    # Return the predicted class
    return predicted_class

def classify_image(image_url, model, class_labels):
    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Open the image and resize it
        img = Image.open(response.raw).convert('RGB').resize((224, 224))

        # Convert the image to a numpy array and preprocess it
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.resnet50.preprocess_input(img_array)

        # Make predictions using the model
        preds = model.predict(img_array)

        # Print raw predictions for debugging
        print("Raw predictions:", preds)

        # Get the image category
        image_type = get_image_category(preds, class_labels)

        return image_type

    except Exception as e:
        print(f"Error classifying image {image_url}: {e}")
        return "Error"
