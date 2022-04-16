#!pip install git+https://github.com/hukkelas/DSFD-Pytorch-Inference.git

import streamlit as st

from face_dectec import faceDetection
from save_img import save_image

import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from streamlit_text_rating.st_text_rater import st_text_rater

from canvas import canvas


im = Image.open("icon.ico")
st.set_page_config(
    page_title="SuperResolution",
    page_icon=im,
    layout="wide",
)

st.title("Super Resolution App")

image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
if image_file is not None:
  save_image(image_file, image_file.name)

  img_file = "uploaded_image/" + image_file.name
  [img_faces, num, boxes] = faceDetection(img_file)
  #st.image(img_faces)

  if len(boxes) > 0:
    canvas(boxes,img_file)
        
  else:
    st.write("NO PERSON DETECTED")
