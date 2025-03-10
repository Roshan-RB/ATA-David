import streamlit as st
from streamlit_cropperjs import st_cropperjs
from streamlit_image_coordinates import streamlit_image_coordinates
import fitz  # PyMuPDF
import tempfile
import os
import PIL
from PIL import Image, ImageDraw
from io import BytesIO
from PIL import ImageDraw
import numpy as np
import easyocr
import pandas as pd
import cv2
import time
import base64
import io
import firebase_admin
from firebase_admin import credentials, firestore
import re


#st.set_page_config(layout="wide")


#Testing 20.06
#st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**Crop Assist**</span>', unsafe_allow_html=True)

# Testing
def main():
	if not firebase_admin._apps:
		cred = credentials.Certificate('serviceAccountkey.json')
		firebase_admin.initialize_app(cred)
	
	if 'selected_dimesions' not in st.session_state:
		st.session_state.selected_dimesions = 0  
		
	fa_css = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <i class="fa-solid fa-bars";></i>
    ''' 
	st.write(fa_css, unsafe_allow_html=True)

	db = firestore.client()
	
	
	def get_collection_names():
		collections = db.collections()
		return [collection.id for collection in collections]
	
	
	collection_name = st.sidebar.selectbox("Select Collection", [""] + get_collection_names())
	
	from streamlit_image_coordinates import streamlit_image_coordinates
	
	import math

	st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**Dimension Manager**</span>', unsafe_allow_html=True)

	
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

		if "ZeichnungsNr" in st.session_state:
			ZeichnungsNr = st.session_state.ZeichnungsNr
		if "cropped_image" in st.session_state:
			cropped_image = st.session_state.cropped_image


	
		scale_str = st.select_slider(
			"Use the slider to adjust the image size to your preference",
			options=["1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7","7.5", "8", "8.5","9","9.5","10"])
		scale = float(scale_str)

		st.warning('Click in this order: Red, then Blue')
		st.warning('Click only on dimensions, avoiding special characters')
		
		if image_with_boxes is not None:
			#print('I entered loop 1')
			width, height = image_with_boxes.size
			new_width_scaled = height/scale
			value = streamlit_image_coordinates(image_with_boxes, width = (width/scale))
		else:
			st.write("Cropped image not found")
		
		#st.write("My favorite color is", scale)
		if image_with_boxes_rotated is not None:
			pass
		else:
			st.write("Cropped image not found")
			
		def point_in_box(x,y,box,scale):
			p0,p1,p2,p3 = box

			min_x = min(p0[0], p1[0], p2[0], p3[0])/scale -20
			max_x = max(p0[0], p1[0], p2[0], p3[0])/scale +20
			min_y = min(p0[1], p1[1], p2[1], p3[1])/scale -20
			max_y = max(p0[1], p1[1], p2[1], p3[1])/scale +20
			return min_x <= x <= max_x and min_y <= y <= max_y
		#value = None   
		if value:
			point = value["x"], value["y"]
			#st.write(value)
			#print('I entered loop 3')
			x,y = value["x"], value["y"]
			#st.write(x,y)
			x1,y1 = rotated_coordinates(x,y,new_width_scaled)
			#st.write(x1,y1) 
			
		try:

			dimension = []
			#global text1 
			#text1 = 0

			if "bounds" in st.session_state:
				#st.write('I entered text 1')
				bounds = st.session_state.bounds
				# Initialize temp and dimension lists
				if "temp" not in st.session_state:
					st.session_state.temp = []
				if "dimension" not in st.session_state:
					st.session_state.dimension = []
				# Initialize highlighted coordinates storage
				if "highlighted_coords" not in st.session_state:
					st.session_state.highlighted_coords = []

				cropped_image_highlighted = st.session_state.image_with_boxes
				#print(type(cropped_image_highlighted))
				cropped_image_highlighted_np = np.array(cropped_image_highlighted)
				total_dimensions = len(bounds)
				for bound in bounds :
					box = [bound[0][0], bound[0][1], bound[0][2], bound[0][3]]		
					#st.write(bound[0])
					if value is not None:
						#st.write('i am trying to read non rotated image')
						if point_in_box(x,y,box,scale):
							try:
								p0, p1, p2, p3 = bound[0]
								# Draw bounding box using OpenCV
								# Store the coordinates
								st.session_state.highlighted_coords.append((p0, p1, p2, p3))

								# Draw bounding box using OpenCV
								for coords in st.session_state.highlighted_coords:
									cv2.line(cropped_image_highlighted_np, coords[0], coords[1], (0, 255, 0), 5)
									cv2.line(cropped_image_highlighted_np, coords[1], coords[2], (0, 255, 0), 5)
									cv2.line(cropped_image_highlighted_np, coords[2], coords[3], (0, 255, 0), 5)
									cv2.line(cropped_image_highlighted_np, coords[3], coords[0], (0, 255, 0), 5)
									#st.write(len(bounds))
								st.session_state.selected_dimesions += 1
								#st.markdown(f'**Percentage of selected Dimensions: {st.session_state.selected_dimesions / total_dimensions}**')
								st.markdown(f'<i class="fa-solid fa-cube" style="margin-right: 10px; font-size: 20px;"></i> <span style="font-size: 24px; color: #3573b3;">**Selected Dimensions**</span>', unsafe_allow_html=True)
								cropped_image_highlighted = Image.fromarray(cropped_image_highlighted_np)
								with st.expander('The previously selected dimesnions are'):
									st.image(cropped_image_highlighted)
							except Exception as e:
								st.write(e)
							global text1
							text1 = bound[1]
							
			if total_dimensions > 0:
				percentage_selected = (st.session_state.selected_dimesions/ total_dimensions) * 100
			else:
				percentage_selected = 0
			st.sidebar.markdown(f'**Percentage of selected dimensions: {percentage_selected:.2f}%**')

			# Add a progress bar
			progress = st.sidebar.progress(0)
			progress.progress(int(percentage_selected))

				

			dimension_rotated = []
			#global text2 
			#text2 = 0
			if "bounds_rotated" in st.session_state:
				#st.write('I entered text 2')
				bounds_rotated = st.session_state.bounds_rotated
				# Initialize temp and dimension lists
				if "temp_rotated" not in st.session_state:
					st.session_state.temp_rotated = []
				if "dimension_rotated" not in st.session_state:
					st.session_state.dimension_rotated = []
				for bound in bounds_rotated :
					box_rotated = [bound[0][0], bound[0][1], bound[0][2], bound[0][3]]
					#st.write("rotated bounds", bound[0])
					if value is not None:
						#st.write('i am trying to read rotated image')
						if point_in_box(x1,y1,box_rotated,scale):
							global text2
							text2 = bound[1]
							##st.write(text2)
				#st.write(text1,text2)
				if text1 is None:
					text1 = str(0.0)
				if text2 is None:
					text2 = str(0.0)
				if text2 != text1:
					# Handle German number formatting (replace comma with dot if present)
					text1 = str(text1)
					text2 = str(text2)
					if ',' in text1:
						text1 = text1.replace(',', '.')
					if ',' in text2:
						text2 = text2.replace(',', '.')
					# Remove trailing periods and ensure no double periods 
					text1 = re.sub(r'\.\.+', '.', text1) # Replace multiple periods with a single period
					text1 = re.sub(r'\.$', '', text1) # Remove trailing period   

					text2 = re.sub(r'\.\.+', '.', text2) 
					text2 = re.sub(r'\.$', '', text2)

					text1 = float(text1)
					text2 = float(text2)
					text = max(text1, text2)
					#st.write('The max value is', text)
				else:
					text = text1
				if len(st.session_state.temp) < 3:
					st.session_state.temp.append(text)
				st.sidebar.write("The selected dimension is: ", text)
				
				
				# When we have two dimensions, add the pair to the main list
				if len(st.session_state.temp) == 2:
					st.session_state.dimension.append(st.session_state.temp[:])
					st.session_state.temp = []
				#st.write(st.session_state.dimension)           
				

				
				if st.session_state.dimension:
					
					
					
					df = pd.DataFrame(st.session_state.dimension, columns=['Width', 'Height'])
					df_sorted = df.sort_index(ascending=False)

					#clear_df = st.sidebar.button("Clear Dataframe")
					#if clear_df:
						#st.session_state.dimension = None
						#df_sorted = st.session_state.df(st.session_state.dimension, columns=['Width', 'Height'])
						
					part_name = st.sidebar.text_input("Part Name:")
					if part_name: 
						st.sidebar.write(f"Part Name entered: {part_name}")
					st.sidebar.data_editor(df, num_rows = "dynamic")
					if "finalize_database" not in st.session_state:
						#st.write('I entered text 2')
						st.session_state.finalize_database = False

					def click_button():
						st.session_state.finalize_database = True

					st.sidebar.button('Finalize Database', on_click=click_button)
					if st.session_state.finalize_database: 
						st.dataframe(df)
						if "upload_button" not in st.session_state:
							#st.write('I entered text 2')
							st.session_state.upload_button = False

						def click_button():
							st.session_state.upload_button = True

						st.button("Upload to Database",on_click=click_button)
						try: 
							if st.session_state.upload_button:
									if st.session_state.dimension:
										#st.write('Ienterd 1')

										# Convert dataframe to a list of dictionaries
										data_to_upload = df.to_dict(orient='records')

										#for record in data_to_upload:
											#record['part_name'] = part_name
										if part_name: 
											data_to_upload[0]['part_name'] = part_name
										#st.write('Ienterd 2')
										# Use the file name as the collection name if it's defined
										if 'ZeichnungsNr' in st.session_state and st.session_state.ZeichnungsNr:
											#st.write('Ienterd 3')
											collection_name = st.session_state.ZeichnungsNr
											# Reference to the Firestore collection
											collection_ref = db.collection(collection_name)

											# Upload each row to the Firestore collection
											for record in data_to_upload:
												#st.write('Ienterd 4')
												collection_ref.add(record)
											#st.write('Ienterd 5')
											st.success(f"Data uploaded to Firebase successfully under collection '{collection_name}'!")
										else:
											st.warning("No file name found for the collection!")

									else:
										st.warning("No data to upload!")
						except Exception as e:
							print(e)

		except Exception as e:

			print('The error for non rotated image is:',str(e))
	except Exception as e:
		print(e)

		st.warning(
			'Please select extract in the main page to detect the text, then come back here to select the required '
			'dimension text!')

	# st.write(f"Zeichnungs- Nr.: {st.session_state.ZeichnungsNr}")

    

if __name__ == "__main__":
    main()
