#!pip install git+https://github.com/hukkelas/DSFD-Pytorch-Inference.git

import streamlit as st

from face_dectec import crop_object, faceDetection
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
    canvas_result_json_data, bg_image  = canvas(boxes,img_file)
    st.write(canvas_result_json_data)
    if canvas_result_json_data is not None:
        
        rst_objects = canvas_result_json_data["objects"]
        objects = pd.json_normalize(canvas_result_json_data["objects"]) # need to convert obj to str because PyArrow
        for rst_objects in rst_objects:
            rts_boxes = [rst_objects['left'],rst_objects['top'],rst_objects['width']+rst_objects['left'],rst_objects['height']+rst_objects['top']]
            #st.write(rts_boxes)
            st.image(crop_object(bg_image, rts_boxes))

        for col in objects.select_dtypes(include=['object']).columns:
            objects[col] = objects[col].astype("str")
        #st.dataframe(objects)
        
  else:
    st.write("NO PERSON DETECTED")
