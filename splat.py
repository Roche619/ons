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

with streamlit_analytics.track():
    image_file = st.file_uploader("Upload an image file", type=["jpg","png","tif"])

    if image_file is not None:
        image_file = Image.open(image_file)
        input_image = np.array(image_file.convert('RGB'))

        resized_image = image_resize(input_image, 25)

        effect = st.sidebar.selectbox("Select type of image manipulation you want to experiment with",
             ["Reflect on Diagonal", "Edge Enhancement", "Modify Adjacent Pixel Values", "Swap RGB Channel Values",
              "Multiplication by Mathematical Constants and Functions", "Splatter Effect"])    

        output_image = resized_image.copy()

        if effect == "Reflect on Diagonal":
            st.markdown("## Reflect on Diagonal")

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
            st.text("- Threshold value determines how the pixel values are assigned")
            st.text("- Value 1 is assigned if the input image pixel value is above the selected threshold")
            st.text("- Value 2 is assigned if the input image pixel value is below the selected threshold")

            threshold = st.sidebar.number_input("Threshold", value=128, min_value=0, max_value=255)
            value_1 = st.sidebar.number_input("Value 1", value=0, min_value=0, max_value=255)
            value_2 = st.sidebar.number_input("Value 2", value=255, min_value=0, max_value=255)

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


        elif effect == "Modify Adjacent Pixel Values":
            st.markdown("## Modify Adjacent Pixel Values") 
            st.text("This takes the values on either side of the current pixel, performs the selected action,")
            st.text("then replaces the current pixel with that new value.")

            np_choice = st.sidebar.selectbox("Select the modification to perform", ["sum", "average", "maximum", "minimum"])
            if np_choice == "sum":
                numpy_func = np.sum
            elif np_choice == "average":
                numpy_func = np.mean
            elif np_choice == "maximum":
                numpy_func = np.max
            elif np_choice == "minimum":
                numpy_func = np.min

            for r in range(resized_image.shape[0]):
                for c in range(resized_image.shape[1]):
                    if(is_outside(r, c, resized_image.shape)):
                        output_image.itemset((r,c,0), 0)
                        output_image.itemset((r,c,1), 0)
                        output_image.itemset((r,c,2), 0)
                    else:
                        output_image.itemset((r,c,0), numpy_func([resized_image.item((r,c,1)), resized_image.item((r,c,2))]))
                        output_image.itemset((r,c,1), numpy_func([resized_image.item((r,c,0)), resized_image.item((r,c,2))]))
                        output_image.itemset((r,c,2), numpy_func([resized_image.item((r,c,0)), resized_image.item((r,c,1))]))
            display_figures(resized_image, output_image)

        elif effect == "Swap RGB Channel Values":
            st.markdown("## Swap RGB Channel Values") 

            channel_choice = st.sidebar.select_slider("Select the channel value", list(range(1,28)))
            if channel_choice == 1:
                c1, c2, c3 = 0, 0, 0
            elif channel_choice == 2:
                c1, c2, c3 = 0, 0, 1
            elif channel_choice == 3:
                c1, c2, c3 = 0, 0, 2
            elif channel_choice == 4:
                c1, c2, c3 = 0, 1, 0
            elif channel_choice == 5:
                c1, c2, c3 = 0, 1, 1
            elif channel_choice == 6:
                c1, c2, c3 = 0, 1, 2
            elif channel_choice == 7:
                c1, c2, c3 = 0, 2, 0
            elif channel_choice == 8:
                c1, c2, c3 = 0, 2, 1
            elif channel_choice == 9:
                c1, c2, c3 = 0, 2, 2
            elif channel_choice == 10:
                c1, c2, c3 = 1, 0, 0
            elif channel_choice == 11:
                c1, c2, c3 = 1, 0, 1
            elif channel_choice == 12:
                c1, c2, c3 = 1, 0, 2
            elif channel_choice == 13:
                c1, c2, c3 = 1, 1, 0
            elif channel_choice == 14:
                c1, c2, c3 = 1, 1, 1
            elif channel_choice == 15:
                c1, c2, c3 = 1, 1, 2
            elif channel_choice == 16:
                c1, c2, c3 = 1, 2, 0
            elif channel_choice == 17:
                c1, c2, c3 = 1, 2, 1
            elif channel_choice == 18:
                c1, c2, c3 = 1, 2, 2
            elif channel_choice == 19:
                c1, c2, c3 = 2, 0, 0
            elif channel_choice == 20:
                c1, c2, c3 = 2, 0, 1
            elif channel_choice == 21:
                c1, c2, c3 = 2, 0, 2
            elif channel_choice == 22:
                c1, c2, c3 = 2, 1, 0
            elif channel_choice == 23:
                c1, c2, c3 = 2, 1, 1
            elif channel_choice == 24:
                c1, c2, c3 = 2, 1, 2
            elif channel_choice == 25:
                c1, c2, c3 = 2, 2, 0
            elif channel_choice == 26:
                c1, c2, c3 = 2, 2, 1
            elif channel_choice == 27:
                c1, c2, c3 = 2, 2, 2

            for r in range(output_image.shape[0]):
                for c in range(output_image.shape[1]):
                    if(is_outside(r, c, resized_image.shape)):
                        output_image.itemset((r,c,0), 0)
                        output_image.itemset((r,c,1), 0)
                        output_image.itemset((r,c,2), 0)
                    else:
                        val_0 = output_image.item((r,c,c1))
                        val_1 = output_image.item((r,c,c2))
                        val_2 = output_image.item((r,c,c3))
                    output_image[r,c] = (val_0,val_1,val_2)
            display_figures(resized_image, output_image)

        elif effect == "Multiplication by Mathematical Constants and Functions":
            st.markdown("## Multiplication by Mathematical Constants and Functions")

            maths_choice = st.sidebar.selectbox("Select the mathematical option to use",
                                                ["e", "pi", "tau", "trig"])
            if maths_choice == "e":
                maths_func = math.e
            elif maths_choice == "pi":
                maths_func = math.pi
            elif maths_choice == "tau":
                maths_func = math.tau
            elif maths_choice == "trig":
                trig_choice = st.sidebar.selectbox("Select the trigonometric function to use", ["sin", "cos", "tan"])
                angle = st.sidebar.slider("Select the angle to use", 0.0, 360.0, 180.0)

                if trig_choice == "sin":
                    maths_func = math.sin(angle)
                elif trig_choice == "cos":
                    maths_func = math.cos(angle)
                elif trig_choice == "tan":
                    maths_func = math.tan(angle)

            for r in range(resized_image.shape[0]):
                for c in range(resized_image.shape[1]):
                    output_image.itemset((r,c,0), resized_image.item((r,c,0)) * maths_func)
                    output_image.itemset((r,c,1), resized_image.item((r,c,1)) * maths_func)
                    output_image.itemset((r,c,2), resized_image.item((r,c,2)) * maths_func)

            display_figures(resized_image, output_image)

        elif effect == "Splatter Effect":
            st.markdown("## Splatter Effect") 

            distribution = st.sidebar.radio("Select type of random distribution to use", ["Uniform", "Normal"])
            diameter = st.sidebar.slider("Select the diameter to use", 0, 100, 20)

            if distribution == "Uniform":
                for r in range(resized_image.shape[0]):
                    for c in range(resized_image.shape[1]):
                        r1 = r + math.ceil(np.random.uniform(-0.5,0.5) * diameter)
                        c1 = c + math.ceil(np.random.uniform(-0.5,0.5) * diameter)

                        if(is_outside(r1, c1, resized_image.shape)):
                            output_image.itemset((r,c,0), 0)
                            output_image.itemset((r,c,1), 0)
                            output_image.itemset((r,c,2), 0)
                        else:
                            output_image.itemset((r,c,0), resized_image.item((r1,c1,0)))
                            output_image.itemset((r,c,1), resized_image.item((r1,c1,1)))
                            output_image.itemset((r,c,2), resized_image.item((r1,c1,2)))

            elif distribution == "Normal":
                for r in range(resized_image.shape[0]):
                    for c in range(resized_image.shape[1]):
                        r1 = r + math.ceil(np.random.normal(-0.5,0.5) * diameter)
                        c1 = c + math.ceil(np.random.normal(-0.5,0.5) * diameter)

                        if(is_outside(r1, c1, resized_image.shape)):
                            output_image.itemset((r,c,0), 0)
                            output_image.itemset((r,c,1), 0)
                            output_image.itemset((r,c,2), 0)
                        else:
                            output_image.itemset((r,c,0), resized_image.item((r1,c1,0)))
                            output_image.itemset((r,c,1), resized_image.item((r1,c1,1)))
                            output_image.itemset((r,c,2), resized_image.item((r1,c1,2)))
            display_figures(resized_image, output_image)