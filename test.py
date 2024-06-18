print(type(str(0.0)))

 else:
                fill_color = color2  # Draw in blue



 def rotated_coordinates(x, y, first_image_height):
            new_x =  y
            new_y = first_image_height - x
            return new_x, new_y
        
        def rotate_all_coordinates(x1, y1, x2, y2, x3, y3, x4, y4, first_image_height):
            x1_rot, y1_rot = rotated_coordinates(x1, y1, first_image_height)
            x2_rot, y2_rot = rotated_coordinates(x2, y2, first_image_height)
            x3_rot, y3_rot = rotated_coordinates(x3, y3, first_image_height)
            x4_rot, y4_rot = rotated_coordinates(x4, y4, first_image_height)
    
            return [[x1_rot, y1_rot], [x2_rot, y2_rot], [x3_rot, y3_rot], [x4_rot, y4_rot]]


        image_with_boxes_rotated = draw_boxes_vertical(image_with_boxes.copy(), bounds_rotated)
        
        def rectangle_dimensions(x1, y1, x2, y2, x3, y3, x4, y4):
            # List to store unique x and y coordinates
            x_coords = [x1, x2, x3, x4]
            y_coords = [y1, y2, y3, y4]
            
            # Find unique x and y coordinates
            unique_x = list(set(x_coords))
            unique_y = list(set(y_coords))
            
            # Calculate width and height
            width = abs(unique_x[1] - unique_x[0])
            height = abs(unique_y[1] - unique_y[0])
            
            # Determine which dimension is larger
            if width > height:
                return 'horizontal'
            elif height > width:
                return 'vertical'

        vertical_dimensions = []
        # Update the coordinates if the condition is met
        for bound in bounds_rotated:
            #print('The bound is', bound[0])
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = bound[0]
            result = rectangle_dimensions(x1,y1,x2,y2,x3,y3,x4,y4)
            #print('result', result)
            if result == 'horizontal':
                vertical_dimensions.append(bound[0])
            #print('The corresponding vertical is', vertical_dimensions)
        #print(vertical_dimensions)
        #print(vertical_dimensions[0])
        #print(vertical_dimensions[0][0])

        for bound in vertical_dimensions:
            [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = bound
            #print('coordinates before rotation', bound)
            new_coords = rotate_all_coordinates(x1, y1, x2, y2, x3, y3, x4, y4, n_height_rot)
            #print('coordinates after rotation', new_coords)
            bound = new_coords
        print(len(vertical_dimensions))
        # Draw the bounding boxes on the image
        result_image = draw_boxes_vertical(image_with_boxes, vertical_dimensions, changed_dim = True)

        st.image(result_image)
        st.session_state.image_with_boxes_rotated = image_with_boxes_rotated