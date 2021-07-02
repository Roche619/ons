import streamlit as st
import streamlit_analytics
from PIL import Image
import numpy as np
import cv2

st.title("Exploring the wonderful world of image manipulation with OpenCV")

image_file = st.file_uploader("Upload an image file", type=["jpg","png","tif"])

if image_file is not None:
    image_file = Image.open(image_file)
    clear_image = np.array(image_file.convert('RGB'))

    if clear_image.shape[1] > 800:
        scale_factor = 50
        height = int(clear_image.shape[0] * scale_factor/100)
        width = int(clear_image.shape[1] * scale_factor/100)
        dimensions = (width,height)

        clear_image = cv2.resize(clear_image, dimensions)
    
    ci = clear_image.copy()
    for r in range(ci.shape[0]):
        for c in range(ci.shape[1]):
            val0 = ci[c,r,0]
            val1 = ci[c,r,1]
            val2 = ci[c,r,2]
            ci[r,c] = (val2,val2,val2)
    
    fly_left, fly_right = st.beta_columns(2)
    with fly_left:
        st.markdown("### Original image")
        st.image(clear_image)
    with fly_right:
        st.markdown("### Processed image")
        st.image(ci)

    st.markdown("#### First few rows of RGB Channels of original image (top row) and processed image (bottom row)")


    title_left, title_center, title_right = st.beta_columns(3)
    with title_left:
        st.write(clear_image[0][:3])
        st.write(ci[0][:3])
    with title_center:
        st.write(clear_image[1][:3])
        st.write(ci[1][:3])
    with title_right:
        st.write(clear_image[2][:3])
        st.write(ci[2][:3])
    