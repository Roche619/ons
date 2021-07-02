import streamlit as st
import streamlit_analytics
from PIL import Image
import numpy as np
import cv2

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
    if st.checkbox("Click to show image"):   
        st.image(clear_image)
    
    ci = clear_image.copy()
    for r in range(ci.shape[0]):
        for c in range(ci.shape[1]):
            val0 = ci[r,c,0]
            val1 = ci[r,c,1]
            val2 = ci[r,c,2]
            ci[r,c] = (val0,val0,val0)
    
    st.image(ci)
            
    title_left, title_center, title_right = st.beta_columns((3))
    
    with title_left:
        st.markdown("### Red Channel")
        st.write(clear_image[0][0])
        st.write(ci[0][0])
    with title_center:
        st.markdown("### Green Channel")
        st.write(clear_image[1][0])
        st.write(ci[1][0])
    with title_right:
        st.markdown("### Blue Channel")
        st.write(clear_image[2][0])
        st.write(ci[2][0])
    