#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:08:38 2021

@author: Eric Gitonga
"""
import streamlit as st
import streamlit_analytics
import cv2
import numpy as np
from PIL import Image

icon = Image.open("images/fly.jpg")

st.set_page_config(
    page_title="Super Basic Photo Editor",
    page_icon=icon,
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Super Basic Photo Editor")

def image_resize(image, scale_factor):
    scale_factor = scale_factor
    height = int(image.shape[0] * scale_factor/100)
    width = int(image.shape[1] * scale_factor/100)
    dimensions = (width,height)

    return cv2.resize(image, dimensions)

def display_figures(img1, img2):
    fig1_left, fig2_right = st.beta_columns(2)
    with fig1_left:
        st.markdown("### Original image")
        st.image(img1)
    with fig2_right:
        st.markdown("### Processed image")
        st.image(img2)

with streamlit_analytics.track():
    image_file = st.file_uploader("Upload an image file", type=["jpg","png","tif"])

    if image_file is not None:
        image_file = Image.open(image_file)
        input_image = np.array(image_file)

        effect = st.sidebar.selectbox("Select type of image manipulation you want to experiment with",
             ["Resize Image", "Flip Image"])
        
        if effect == "Resize Image":
            sf1 = st.sidebar.slider("Select the scale factor to use in resizing image", 0.1, 30.0, 15.0)
            output_image = image_resize(input_image, sf1)

        if effect == "Flip Image":
            mirror_choice = st.sidebar.selectbox("Choose  how to flip the image",
                                 ["Horizontally", "Vertically", "Both"])
            if mirror_choice == "Horizontally":
                output_image = cv2.flip(input_image,1)
            elif mirror_choice == "Vertically":
                output_image = cv2.flip(input_image,0)
            else:
                output_image = cv2.flip(input_image,-1)
            
#        if st.button("Process Image"):
#            display_figures(input_image, output_image)
        display_figures(input_image, output_image)
