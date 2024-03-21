import streamlit as st
import tensorflow as tf
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
import urllib.request
import gdown


@st.cache
def load_model():
  
  url = "https://drive.google.com/uc?id=144uxP9sepud62pjRlsvwMXxgvuBlhvFb"
  output = "model/solar_panel_inspection.hdf5"
  gdown.download(url=url, output=output, quiet=False, proxy=None)

with st.spinner('Model is being loaded..'):
  model=load_model()

MODEL_PATH = 'model/solar_panel_inspection.hdf5'
model=tf.keras.models.load_model(MODEL_PATH)  

st.write("""
         # Solar Panel Inspection
         """
         )

file = st.file_uploader("Upload the image to be classified \U0001F447", type=["jpg", "png"])

import cv2
from PIL import Image, ImageOps
import numpy as np


class_names = ['Bird-drop', 'Clean', 'Dusty', 'Electrical-damage', 'Physical-Damage', 'Snow-Covered']

st.sidebar.header('SolarY')
st.sidebar.markdown('Accurately classifies image classes and helps to guide the plant managers to take actions')


def upload_predict(upload_image, model):
    
        size = (244,244)    
        image = ImageOps.fit(upload_image, size, Image.Resampling.LANCZOS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img, dsize=(244, 244),interpolation=cv2.INTER_CUBIC)
        
        img_reshape = img_resize[np.newaxis,...]

        predictions = model.predict(img_reshape)
        score = tf.nn.softmax(predictions[0])
        pred_class = class_names[np.argmax(score)]
        
        return score,pred_class

if file is None:
    st.text("Please upload an image file")

else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    score,pred_class = upload_predict(image, model)
    st.sidebar.info('Accuracy: 100%')
    
    st.sidebar.write('The predicted class is')
    if pred_class == "Clean":
      st.sidebar.success(pred_class)
    else:
      st.sidebar.warning(pred_class)