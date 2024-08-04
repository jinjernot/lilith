import numpy as np
import requests
from PIL import Image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image

def get_image_category(decoded_preds):
    """
    Determine the category of an image based on its predictions.
    
    Args:
    - decoded_preds (list): A list of tuples containing prediction information.

    Returns:
    - str: The category of the image.
    """
    # Define specific categories and keywords
    categories = {
        "laptop": ["laptop", "notebook"],
        "desktop": ["desktop"],
        "printer": ["printer"],
    }

    # Iterate over decoded predictions
    for _, name, _ in decoded_preds:
        # Check each category against prediction keywords
        for category, keywords in categories.items():
            if any(keyword in name.lower() for keyword in keywords):
                return category.capitalize()

    # Return "Other" if no category is matched
    return "Other"

def classify_image(image_url, model):
    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Open the image and resize it
        img = Image.open(response.raw).convert('RGB').resize((224, 224))

        # Convert the image to a numpy array and preprocess it
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Make predictions using the model
        preds = model.predict(img_array)
        decoded_preds = decode_predictions(preds, top=3)[0]

        # Get the image category
        image_type = get_image_category(decoded_preds)

        return image_type

    except Exception as e:
        print(f"Error classifying image {image_url}: {e}")
        return "Error"
