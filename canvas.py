import json
import streamlit as st

from face_dectec import crop_object

import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas


list = []
filename = 'saved_state.json'

@st.cache()
def canvas(boxes,img_file):
    for boxes in boxes:
        list.append({
        "type": "rect",
            "left": boxes[0],
            "top": boxes[1],
            "width": boxes[2]-boxes[0],
            "height": boxes[3]-boxes[1],
            "fill": "#00ff0050",
            "stroke": "#00ff00",
            "strokeWidth": 3
        })

    # Verify updated list
    #st.write(list)

    listObj = {
        "version": "4.4.0",
        "objects": list  
    }

    # Verify updated listObj
    #st.write(listObj)

    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))

    with open(filename, "r") as f:   saved_state = json.load(f)
    #st.write(saved_state)

    bg_image = Image.open(img_file)
    label_color = (
        st.sidebar.color_picker("Annotation color: ", "#00ff00") + "50"
    )  # for alpha from 00 to FF
    tool_mode = st.sidebar.selectbox(
        "Select tool:", ("draw", "move")
    )
    mode = "transform" if tool_mode=="move" else "rect"

    canvas_result = st_canvas(
        fill_color=label_color,
        stroke_width=3,
        stroke_color="#00ff00",
        background_image=bg_image,
        height=bg_image.height,
        width=bg_image.width,
        initial_drawing=saved_state,
        drawing_mode=mode,
        key="color_annotation_app",
    )
    return canvas_result, bg_image 


