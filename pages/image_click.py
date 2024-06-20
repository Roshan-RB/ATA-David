import streamlit as st
from streamlit_cropperjs import st_cropperjs
from streamlit_image_coordinates import streamlit_image_coordinates
import fitz  # PyMuPDF
import tempfile
import os
import PIL
from PIL import Image
from io import BytesIO
from PIL import ImageDraw
import numpy as np
import easyocr
import pandas as pd
import cv2
import time
import base64
import io

st.set_page_config(layout="wide")

from streamlit_image_coordinates import streamlit_image_coordinates

import math

def rotated_coordinates(x, y, first_image_height):
    """
    Rotates the point (x, y) in the first image by 270 degrees
    to find the corresponding point in the second image.
    Args:
    x (int): The x-coordinate of the point in the first image.
    y (int): The y-coordinate of the point in the first image.
    first_image_height (int): The height of the first image (default is 473).
    second_image_height (int): The height of the second image (default is 1246).
	
	Returns:
    tuple: The corresponding (x, y) coordinates in the second image.
    """
    new_x = first_image_height - y
    new_y = x
    return new_x, new_y
	
	try:
    # Check if the image is in session state
    if 'image_with_boxes' in st.session_state:
        # Retrieve the image from session state
        image_with_boxes = st.session_state.image_with_boxes
    else:
        st.write("No image found in session state.")
    # Check if the image is in session state
    if 'image_with_boxes_rotated' in st.session_state:
        # Retrieve the image from session state
        image_with_boxes_rotated = st.session_state.image_with_boxes_rotated
    else:
        st.write("No image found in session state.")
    scale_str = st.select_slider(
        "Select scaling factor to downsize the image",
        options=["1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7","7.5", "8", "8.5","9","9.5","10"])
    scale = float(scale_str)
	
	if image_with_boxes is not None:
        #print('I entered loop 1')
        width, height = image_with_boxes.size
        new_width_scaled = height/scale
        value = streamlit_image_coordinates(image_with_boxes, width = (width/scale))
    else:
        st.write("No image found in session state.")
    
    #st.write("My favorite color is", scale)
    if image_with_boxes_rotated is not None:
        pass
    else:
        st.write("No image found in session state.")
		
		def point_in_box(x,y,box,scale):
        p0,p1,p2,p3 = box
  
        min_x = min(p0[0], p1[0], p2[0], p3[0])/scale -20
        max_x = max(p0[0], p1[0], p2[0], p3[0])/scale +20
        min_y = min(p0[1], p1[1], p2[1], p3[1])/scale -20
        max_y = max(p0[1], p1[1], p2[1], p3[1])/scale +20
        return min_x <= x <= max_x and min_y <= y <= max_y
    #value = None   
    if value:
        #st.write(value)
        #print('I entered loop 3')
        x,y = value["x"], value["y"]
        #st.write(x,y)
        x1,y1 = rotated_coordinates(x,y,new_width_scaled)
        #st.write(x1,y1) 
		
		try:

        dimension = []
        global text1 
        text1 = 0
  
        if "bounds" in st.session_state:
            bounds = st.session_state.bounds
            # Initialize temp and dimension lists
            if "temp" not in st.session_state:
                st.session_state.temp = []
            if "dimension" not in st.session_state:
                st.session_state.dimension = []
            for bound in bounds :
                box = [bound[0][0], bound[0][1], bound[0][2], bound[0][3]]
                if value is not None:
                    #st.write('i am trying to read non rotated image')
                    if point_in_box(x,y,box,scale):
                        text1 = bound[1]
                        #st.write(text1)
        dimension_rotated = []
        global text2 
        text2 = 0
        if "bounds_rotated" in st.session_state:
            bounds_rotated = st.session_state.bounds_rotated
            # Initialize temp and dimension lists
            if "temp_rotated" not in st.session_state:
                st.session_state.temp_rotated = []
            if "dimension_rotated" not in st.session_state:
                st.session_state.dimension_rotated = []
            for bound in bounds_rotated :
				box_rotated = [bound[0][0], bound[0][1], bound[0][2], bound[0][3]]
                if value is not None:
                    #st.write('i am trying to read rotated image')
                    if point_in_box(x1,y1,box_rotated,scale):
                        text2 = bound[1]
                        ##st.write(text2)
            #st.write(text1,text2)
            if text1 is None:
                text1 = str(0.0)
            if text2 is None:
                text2 = str(0.0)
            if text2 != text1:
                # Handle German number formatting (replace comma with dot if present)
                if ',' in text1:
                    text1 = text1.replace(',', '.')
                if ',' in text2:
                    text2 = text2.replace(',', '.')
                    
                text1 = float(text1)
                text2 = float(text2)
                text = max(text1, text2)
                #st.write('The max value is', text)
            else:
                text = text1
            if len(st.session_state.temp) < 3:
                st.session_state.temp.append(text)
        
            # When we have two dimensions, add the pair to the main list
            if len(st.session_state.temp) == 2:
                st.session_state.dimension.append(st.session_state.temp[:])
                st.session_state.temp = []
            #st.write(st.session_state.dimension)           
            st.warning('Please click in the following order: Red , Blue')
            st.warning('Please click only on dimensions and not on special characters')
			
			if st.session_state.dimension:
                #st.write('Selected dimension pairs: ', st.session_state.dimension)
                df = pd.DataFrame(st.session_state.dimension, columns=['Width', 'Height'])
                #st.write('DataFrame of Selected Dimensions:')
                #st.write('df1')

                st.data_editor(df[1:])


    except Exception as e:
  
        print('The error for non rotated image is:',str(e))
except Exception as e:
    print(e)

    st.warning('Please select extract in the main page to detect the text, then come back here to select the required dimension text!')
			
			
                
