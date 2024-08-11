import tensorflow as tf

model = tf.keras.models.load_model('models/fine_tuned_resnet50.keras')

class_labels = ['ink cartridge']  