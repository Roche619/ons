import streamlit as st
import streamlit_analytics
from PIL import Image
import numpy as np
import cv2
import math

st.title("Exploring the wonderful world of image manipulation with OpenCV and NumPy")

def image_resize(image, scale_factor):
    scale_factor = scale_factor
    height = int(image.shape[0] * scale_factor/100)
    width = int(image.shape[1] * scale_factor/100)
    dimensions = (width,height)

    return cv2.resize(image, dimensions)    

def is_outside(r, c, shape):
    if(c < 0 or c >= shape[1]):
        return True
    if(r < 0 or r >= shape[0]):
        return True
    else:
        return False
    
def display_figures(img1, img2):
    fig1_left, fig2_right = st.beta_columns(2)
    with fig1_left:
        st.markdown("### Original image")
        st.image(img1)
    with fig2_right:
        st.markdown("### Processed image")
        st.image(img2)

image_file = st.file_uploader("Upload an image file", type=["jpg","png","tif"])

if image_file is not None:
    image_file = Image.open(image_file)
    input_image = np.array(image_file.convert('RGB'))

    sf1 = st.sidebar.slider("Enter the scale factor to use in resizing image", 0.0, 100.0, 100.0)
    resized_image = image_resize(input_image, sf1)
    
    effect = st.sidebar.selectbox("Select type of image manipulation you want to experiment with",
         ["Reflect on Diagonal", "Edge Enhancement"])    
    
    if effect == "Reflect on Diagonal":
        st.markdown("## Reflect on Diagonal")

        output_image = resized_image.copy()
        dim = output_image.shape[0]
        output_image = output_image[:dim,:dim,:3]
        for r in range(output_image.shape[0]):
            for c in range(output_image.shape[1]):
                if(is_outside(r, c, resized_image.shape)):
                    output_image.itemset((r,c,0), 0)
                    output_image.itemset((r,c,1), 0)
                    output_image.itemset((r,c,2), 0)
                else:
                    val_0 = output_image.item((c,r,0))
                    val_1 = output_image.item((c,r,1))
                    val_2 = output_image.item((c,r,2))

                output_image[r,c] = (val_0,val_1,val_2)
    
        display_figures(resized_image, output_image)
       
    elif effect == "Edge Enhancement":
        st.markdown("## Edge Enhancement") 
    
        st.sidebar.markdown("### Select the values for threshold, value_1 and value_2 to modify the image")
        threshold = st.sidebar.number_input("Input the threshold value", value=128, min_value=0, max_value=255)
        value_1 = st.sidebar.number_input("Input value 1", value=0, min_value=0, max_value=255)
        value_2 = st.sidebar.number_input("Input value 2", value=255, min_value=0, max_value=255)
    
        output_image = resized_image.copy()

        for r in range(resized_image.shape[0]):
            for c in range(resized_image.shape[1]):
                if resized_image.item((r,c,1)) >= threshold:
                    r1 = value_1
                else:
                    r1 = value_2
                if resized_image.item((r,c,1)) >= threshold:
                    c1 = value_1
                else:
                    c1 = value_2
                
                if(is_outside(r1, c1, resized_image.shape)):
                    output_image.itemset((r,c,0), 0)
                    output_image.itemset((r,c,1), 0)
                    output_image.itemset((r,c,2), 0)
                else:
                    output_image.itemset((r,c,0), resized_image.item((r1,c1,0)))
                    output_image.itemset((r,c,1), resized_image.item((r1,c1,1)))
                    output_image.itemset((r,c,2), resized_image.item((r1,c1,2)))
        display_figures(resized_image, output_image)