from io import BytesIO
from pathlib import Path

import tensorflow as tf
import tensorflow.keras as keras

SIZE = 224
DEVICE = "/CPU:0"

tags = []
with open(str(Path(__file__).parent / "tags.txt")) as f:
    while line := f.readline():
        if striped := line.strip():
            tags.append(striped)

# print(len(tags))

with tf.device(DEVICE):
    base_model = keras.applications.resnet.ResNet50(
        include_top=False, weights=None, input_shape=(SIZE, SIZE, 3)
    )
    model = keras.Sequential(
        [
            base_model,
            keras.layers.Conv2D(filters=len(tags), kernel_size=(1, 1), padding="same"),
            keras.layers.BatchNormalization(epsilon=1.001e-5),
            keras.layers.GlobalAveragePooling2D(name="avg_pool"),
            keras.layers.Activation("sigmoid"),
        ]
    )
    model.load_weights(str(Path(__file__).parent / "model-resnet_custom_v3.h5"))


@tf.function
def process_data(content):
    img = tf.io.decode_jpeg(content, channels=3)
    img = tf.image.resize_with_pad(img, SIZE, SIZE, method="nearest")
    img = tf.image.resize(img, (SIZE, SIZE), method="nearest")
    img = img / 255
    return img


def predict(content):
    with tf.device(DEVICE):
        data = process_data(content)
        data = tf.expand_dims(data, 0)
        out = model(data)[0]
    return dict((tags[i], out[i].numpy()) for i in range(len(tags)))


def predict_file(file: BytesIO, limit: float):
    data = predict(file.read())
    ret = filter(lambda x: x[1] > limit, data.items())
    ret = map(lambda x: (x[0], float(x[1])), ret)
    return dict(ret)
