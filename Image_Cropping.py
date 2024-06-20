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




fa_css = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
<i class="fa-solid fa-bars";></i>
''' 
st.write(fa_css, unsafe_allow_html=True)


reader = easyocr.Reader(['en'])

#Testing 20.06

st.title("Dimension Detection!")
# Initialize session state variables
if 'pdf_file' not in st.session_state:
    st.session_state.pdf_file = None
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'image_with_boxes' not in st.session_state:
    st.session_state.image_with_boxes = None
if 'bounds' not in st.session_state:
    st.session_state.bounds = None
if 'cropped_image' not in st.session_state:
    st.session_state.cropped_image = None
if 'Processed_image' not in st.session_state:
    st.session_state.Processed_image = None
if 'crop_button_clicked' not in st.session_state:
    st.session_state.crop_button_clicked = False
if 'pil_image' not in st.session_state:
    st.session_state.pil_image = None
if 'rotatedimg' not in st.session_state:
    st.session_state.rotatedimg = None
if 'tmp_file_path' not in st.session_state:
 st.session_state.tmp_file_path = None
if 'pdf_document' not in st.session_state:
    st.session_state.pdf_document  = None
if 'bounds_rotated' not in st.session_state:
    st.session_state.bounds_rotated = None
if 'image_with_boxes_rotated' not in st.session_state:
    st.session_state.image_with_boxes_rotated  = None


pdf_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")
page_number = st.sidebar.number_input("Enter the page number:", min_value=1, format="%d", value=1)



def preprocess(img):
     # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #st.image( gray, caption='grayscale_image', use_column_width='never')
    # Get the dimensions of the grayscale image
    height, width = gray.shape[:2]
    #st.write("Image Size (Width x Height):", width, "x", height)
    # Calculate the new width and height by multiplying current dimensions by 2
    new_width = width * 4
    new_height = height * 4
    #st.write("Image Size (Width x Height):", new_width, "x", new_height)
    # Resize the grayscale image
    resized_gray = cv2.resize(gray, (new_width, new_height))
    #thresholded_resized_image = cv2.adaptiveThreshold(resized_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    return resized_gray


if pdf_file:
    st.session_state.pdf_file = pdf_file

if st.session_state.pdf_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(st.session_state.pdf_file.read())
        tmp_file_path = tmp_file.name
    st.session_state.tmp_file_path = tmp_file_path
    try:
        pdf_document = fitz.open(st.session_state.tmp_file_path)
        st.session_state.pdf_document  = pdf_document

        if page_number > len(st.session_state.pdf_document):
            st.error(f"Invalid page number. Maximum page number is {len(st.session_state.pdf_document)}.")
        else:
            st.session_state.page_number = page_number
            page = st.session_state.pdf_document.load_page(st.session_state.page_number - 1)
            image_bytes = page.get_pixmap().tobytes()
            st.session_state.image_bytes = image_bytes

            # Display the PDF page
            st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**PDF**</span>', unsafe_allow_html=True)
            st.image(st.session_state.image_bytes, use_column_width=True, caption=f"Page {page_number}")

            # Use cropper to select and crop a part of the image only if the page number changes
            if st.button("Select area to crop"):
                st.session_state.crop_button_clicked = True
    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.pdf_file = None  # Clear the uploaded PDF file
    if st.session_state.crop_button_clicked:
        cropped_image = st_cropperjs(st.session_state.image_bytes, btn_text="Crop Image")
        if cropped_image:
            st.session_state.cropped_image = cropped_image
            with st.spinner("Loading the cropped image..."):
                time.sleep(5)
            st.success("You can extract the text now !")
            try:
                # Convert cropped image to PIL Image
                pil_image = Image.open(BytesIO(st.session_state.cropped_image))
                st.session_state.pil_image = pil_image
                # Display the cropped image
                st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**Cropped Image**</span>', unsafe_allow_html=True)
                #st.image(st.session_state.pil_image, use_column_width='auto')
                width, height = st.session_state.pil_image.size
                #st.write("Image Size (Width x Height):", width, "x", height)



                # Save the cropped image as a PNG file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img_file:
                    st.session_state.pil_image.save(tmp_img_file.name)
                    # Read the cropped image back as bytes
                    with open(tmp_img_file.name, "rb") as img_file:
                        img_bytes = img_file.read()

                    # Provide download button for the cropped image
                    #st.download_button("Download Cropped Image", img_bytes, file_name="cropped_image.png", mime="image/png")

            except Exception as e:
                st.error(f"Error: {e}")


    #if st.session_state.pdf_file:
        #try:
            #st.session_state.pdf_document.close()  # Close the PDF document
            #os.unlink(tmp_file_path)  # Clean up the temporary file
        #except Exception as e:
            #st.error(f"Error during cleanup: {e}")

else:
    st.write("Upload a PDF file using the file uploader above.")




if st.session_state.pil_image:



    def rotate_image(im, angle):
        return im.rotate(angle, expand=True)

    image_np = np.array(st.session_state.pil_image)

    thresholded_resized_image = preprocess(image_np)

###code for non rotated image 

    st.image(thresholded_resized_image)

    # Convert NumPy array back to PIL Image
    Processed_Image = Image.fromarray(thresholded_resized_image)
    #st.image(Processed_Image)
    st.write('')
    #st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**Processed Image**</span>', unsafe_allow_html=True)
    #st.image(Processed_Image, use_column_width='auto')

    n_width, n_height = Processed_Image.size
    #st.write("Image Size (Width x Height):", n_width, "x", n_height)



     # Convert PIL Image to JPEG format
    img_byte_arr = BytesIO()
    Processed_Image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()



    # Doing OCR. Get bounding boxes.
    bounds = reader.readtext(img_byte_arr,
                            allowlist="0123456789,",
                            blocklist="qwertzuioplkjhgfdsayxcvbnm:.;()-_#'+*?=/&%$§![]",
                            text_threshold = 0.4,
                            add_margin = 0.2
                            )
    #st.write(bounds)
    
    if bounds not in st.session_state:
        st.session_state.bounds = bounds

    def draw_boxes_horizontal(image, bounds, color1='red', color2='blue', width=4):
        rgb_image = Image.new('RGB', image.size)
        rgb_image.paste(image)
        draw = ImageDraw.Draw(rgb_image)
        
        for bound in bounds:
            p0, p1, p2, p3 = bound[0]
            
            x1, y1 = p0
            x2, y2 = p2
            
            # Calculate aspect ratios
            aspect_ratio1 = (x2 - x1) / (y2 - y1)
            aspect_ratio2 = (y2 - y1) / (x2 - x1)
            
            # Determine color based on aspect ratio
            if aspect_ratio1 > aspect_ratio2:
                fill_color = color1  # Draw in red
                # Draw bounding box
                draw.line([*p0, *p1, *p2, *p3, *p0], fill=fill_color, width=width)
            else:
                fill_color = color2  # Draw in red
                # Draw bounding box
                draw.line([*p0, *p1, *p2, *p3, *p0], fill=fill_color, width=width)
        return rgb_image
    
    def draw_boxes_vertical(image, bounds, color1='red', color2='blue', width=4, changed_dim = False):
        rgb_image = Image.new('RGB', image.size)
        rgb_image.paste(image)
        draw = ImageDraw.Draw(rgb_image)
        if changed_dim is False:
            for bound in bounds:
                p0, p1, p2, p3 = bound[0]
                
                x1, y1 = p0
                x2, y2 = p2
                
                # Calculate aspect ratios
                aspect_ratio1 = (x2 - x1) / (y2 - y1)
                aspect_ratio2 = (y2 - y1) / (x2 - x1)
                
                # Determine color based on aspect ratio
                if aspect_ratio1 > aspect_ratio2:
                    fill_color = color2  # blue
                    # Draw bounding box
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=fill_color, width=width)
            
            return rgb_image
        else:
            for bound in bounds:
                print('The artificaial hor dim is',bound)
                p0, p1, p2, p3 = bound
                fill_color = color2
                draw.line([*p0, *p1, *p2, *p3, *p0], fill=fill_color, width=width)
            
            return rgb_image
    st.session_state.rotatedimg = rotate_image(st.session_state.pil_image, 270)
    image_np_rotated = np.array(st.session_state.rotatedimg)
    thresholded_resized_image_rotated = preprocess(image_np_rotated)
    #st.image(thresholded_resized_image_rotated)
    # Gaussian blur
    #blur = cv2.GaussianBlur(equ, (5, 5), 1)
    # Convert NumPy array back to PIL Image
    Processed_Image_rot = Image.fromarray(thresholded_resized_image_rotated)
    #st.image(Processed_Image_rot)
    st.write('')
    #st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**Processed Image**</span>', unsafe_allow_html=True)
    #st.image(Processed_Image_rot, use_column_width='auto')
    n_width_rot, n_height_rot = Processed_Image_rot.size
    #st.write("Image Size (Width x Height):", n_width, "x", n_height)
     # Convert PIL Image to JPEG format
    img_byte_arr_rot = BytesIO()
    Processed_Image_rot.save(img_byte_arr_rot, format='PNG')
    img_byte_arr_rot = img_byte_arr_rot.getvalue()
    # Doing OCR. Get bounding boxes.
    bounds_rotated = reader.readtext(img_byte_arr_rot,
                            allowlist="0123456789,",
                            blocklist="qwertzuioplkjhgfdsayxcvbnm:.;-_#()'+*?=/&%$§![]"
                            )
    #st.write(bounds)
    
    if bounds_rotated not in st.session_state:
        st.session_state.bounds_rotated = bounds_rotated












    if st.button('Extract_text'):
        st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**OCR**</span>', unsafe_allow_html=True)
        with st.spinner('Extracting text...'):
            time.sleep(8)

        image_with_boxes = draw_boxes_horizontal(Processed_Image.copy(), bounds)
        #print(image_with_boxes.size)
        #st.image(image_with_boxes)
        st.session_state.image_with_boxes = image_with_boxes


        if 'image_with_boxes' in st.session_state:
            st.image(st.session_state.image_with_boxes, use_column_width= 'auto')


        #st.image(rotated_image_with_boxes, use_column_width= "auto"




        #st.write('Extracted text:')

        ##correctly detects the vertical dimesnions
        image_with_boxes_rotated = draw_boxes_vertical(Processed_Image_rot.copy(), bounds_rotated)
        #print(image_with_boxes_rotated.size)
        #st.image(image_with_boxes_rotated)

        st.session_state.image_with_boxes_rotated = image_with_boxes_rotated
