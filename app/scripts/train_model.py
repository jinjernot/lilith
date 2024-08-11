import os
import requests
from PIL import Image
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Function to download images
def download_images(image_urls, save_dir, class_name):
    class_dir = os.path.join(save_dir, class_name)
    os.makedirs(class_dir, exist_ok=True)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')
            img.save(os.path.join(class_dir, f"{class_name}_{i}.jpg"))
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Example usage
image_urls = [
    'https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c08996948.png',
    'https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c08477602.png',
    'https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c09008679.jpg'
]
download_images(image_urls, 'data', 'cartridge_box')

# Data generators
train_dir = 'data'

train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Define the model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    epochs=10
)

# Save the model in Keras format
model.save('models/fine_tuned_resnet50.keras')

# Load the model
loaded_model = tf.keras.models.load_model('models/fine_tuned_resnet50.keras')
