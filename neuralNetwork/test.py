from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

img_width=224
img_height=224

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

# predicting images
img = image.load_img('v_data/test/planes/1.jpg', target_size=(img_width, img_height))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
images = np.vstack([x])
classes = model.predict_classes(images, batch_size=10)
print(classes)

# predicting multiple images at once
#img = image.load_img('test2.jpg', target_size=(img_width, img_height))
#y = image.img_to_array(img)
#y = np.expand_dims(y, axis=0)

# pass the list of multiple images np.vstack()
#images = np.vstack([x, y])
#classes = model.predict_classes(images, batch_size=10)

# print the classes, the images belong to
#print classes
#print classes[0]
#sprint classes[0][0]
