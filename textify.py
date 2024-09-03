import cv2
import numpy as np

class TextOverlay:
    def __init__(self, image):
        """
        Initialize the TextOverlay object with an image.

        :param image: The image on which text overlay will be applied. It should be a valid image array (NumPy ndarray).
        """
        if not isinstance(image, np.ndarray):
            raise TypeError("The image must be a NumPy ndarray.")
        
        self.image = image
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.0  # Default font scale for visibility
        self.font_color = (0, 0, 0)  # Default color: Black
        self.thickness = 2
        self.line_type = cv2.LINE_AA
        self.margin = 20  # Margin around the text block
        self.padding = 20  # Padding between lines of text
        self.bg_padding = 10  # Padding within the background box around text
        self.corner_radius = 10  # Radius for rounded corners of the background box
        self.background_color = (255, 255, 255)  # Default background color: White

    def set_text_properties(self, font_scale=1.0, font_color=(0, 0, 0), thickness=2, background_color=(255, 255, 255)):
        """
        Set properties for the text overlay.

        :param font_scale: Scale of the font.
        :param font_color: Color of the font in (B, G, R) format.
        :param thickness: Thickness of the font.
        :param background_color: Background color of the text in (B, G, R) format.
        """
        self.font_scale = font_scale
        self.font_color = font_color
        self.thickness = thickness
        self.background_color = background_color

    def draw_rounded_rectangle(self, start_point, end_point, radius, color, thickness=-1):
        """
        Draw a rounded rectangle on the image.

        :param start_point: Top-left corner of the rectangle.
        :param end_point: Bottom-right corner of the rectangle.
        :param radius: Radius of the rounded corners.
        :param color: Color of the rectangle in (B, G, R) format.
        :param thickness: Thickness of the rectangle borders. Use -1 for filled rectangle.
        """
        # Vertices for the rectangle with rounded corners
        vertices = np.array([
            [start_point[0] + radius, start_point[1]],
            [end_point[0] - radius, start_point[1]],
            [end_point[0], start_point[1] + radius],
            [end_point[0], end_point[1] - radius],
            [end_point[0] - radius, end_point[1]],
            [start_point[0] + radius, end_point[1]],
            [start_point[0], end_point[1] - radius],
            [start_point[0], start_point[1] + radius]
        ], dtype=np.int32)

        # Draw the filled polygon
        cv2.fillPoly(self.image, [vertices], color)

        # Draw the rounded corners
        cv2.ellipse(self.image, (start_point[0] + radius, start_point[1] + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(self.image, (end_point[0] - radius, start_point[1] + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(self.image, (end_point[0] - radius, end_point[1] - radius), (radius, radius), 0, 0, 90, color, thickness)
        cv2.ellipse(self.image, (start_point[0] + radius, end_point[1] - radius), (radius, radius), 90, 0, 90, color, thickness)

    def draw_bbox(self, bbox, color, thickness=2):
        """
        Draw a bounding box with rounded corners around a specified area.

        :param bbox: Bounding box coordinates in the format [x, y, width, height].
        :param color: Color of the bounding box in (B, G, R) format.
        :param thickness: Thickness of the bounding box lines.
        """
        thickness += 1
        start_point = (bbox[0], bbox[1])
        end_point = (bbox[0] + bbox[2], bbox[1] + bbox[3])
        radius = self.corner_radius

        # Coordinates of the rectangle's corners
        top_left = start_point
        top_right = (end_point[0], start_point[1])
        bottom_left = (start_point[0], end_point[1])
        bottom_right = end_point

        # Draw straight lines for the edges
        cv2.line(self.image, (top_left[0] + radius, top_left[1]), (top_right[0] - radius, top_right[1]), color, thickness)
        cv2.line(self.image, (top_right[0], top_right[1] + radius), (bottom_right[0], bottom_right[1] - radius), color, thickness)
        cv2.line(self.image, (bottom_right[0] - radius, bottom_right[1]), (bottom_left[0] + radius, bottom_left[1]), color, thickness)
        cv2.line(self.image, (bottom_left[0], bottom_left[1] - radius), (top_left[0], top_left[1] + radius), color, thickness)

        # Draw the arcs at the corners
        cv2.ellipse(self.image, (top_left[0] + radius, top_left[1] + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(self.image, (top_right[0] - radius, top_right[1] + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(self.image, (bottom_right[0] - radius, bottom_right[1] - radius), (radius, radius), 0, 0, 90, color, thickness)
        cv2.ellipse(self.image, (bottom_left[0] + radius, bottom_left[1] - radius), (radius, radius), 90, 0, 90, color, thickness)


    def put_text(self, texts, bbox=None, position='inside_top_left', bbox_color=(0, 255, 0)):
        """
        Add text to the image within or outside a bounding box.

        :param texts: List of text strings to be displayed.
        :param bbox: Bounding box coordinates in the format [x, y, width, height]. If None, the entire image is used as the bounding box.
        :param position: Position of the text relative to the bounding box. 
                         Available options: 'inside_top_left', 'inside_top_center', 'inside_top_right', 
                                            'inside_bottom_left', 'inside_bottom_center', 'inside_bottom_right', 
                                            'outside_top_left', 'outside_top_center', 'outside_top_right', 
                                            'outside_bottom_left', 'outside_bottom_center', 'outside_bottom_right', 
                                            'outside_left', 'outside_right'.
        :param bbox_color: Color of the bounding box in (B, G, R) format.
        :return: The image (frame) with the applied text and bounding box.
        """
        if bbox:
            self.draw_bbox(bbox, bbox_color, self.thickness)
        else:
            h, w, _ = self.image.shape
            bbox = [0, 0, w, h]  # Default to the full image as the bounding box

        # Calculate text sizes and total dimensions
        text_sizes = [cv2.getTextSize(text, self.font, self.font_scale, self.thickness)[0] for text in texts]
        max_text_width = max(size[0] for size in text_sizes) + 2 * self.bg_padding
        total_text_height = sum(size[1] for size in text_sizes) + (len(texts) - 1) * self.padding + 2 * self.bg_padding

        # Define possible text positions relative to the bounding box
        positions = {
            'inside_top_left': (bbox[0] + self.margin, bbox[1] + self.margin),
            'inside_top_center': (bbox[0] + (bbox[2] - max_text_width) // 2, bbox[1] + self.margin),
            'inside_top_right': (bbox[0] + bbox[2] - max_text_width - self.margin, bbox[1] + self.margin),
            'inside_bottom_left': (bbox[0] + self.margin, bbox[1] + bbox[3] - total_text_height - self.margin),
            'inside_bottom_center': (bbox[0] + (bbox[2] - max_text_width) // 2, bbox[1] + bbox[3] - total_text_height - self.margin),
            'inside_bottom_right': (bbox[0] + bbox[2] - max_text_width - self.margin, bbox[1] + bbox[3] - total_text_height - self.margin),
            'outside_top_left': (bbox[0] + self.margin, bbox[1] - total_text_height - self.margin),
            'outside_top_center': (bbox[0] + (bbox[2] - max_text_width) // 2, bbox[1] - total_text_height - self.margin),
            'outside_top_right': (bbox[0] + bbox[2] - max_text_width - self.margin, bbox[1] - total_text_height - self.margin),
            'outside_bottom_left': (bbox[0] + self.margin, bbox[1] + bbox[3] + self.margin),
            'outside_bottom_center': (bbox[0] + (bbox[2] - max_text_width) // 2, bbox[1] + bbox[3] + self.margin),
            'outside_bottom_right': (bbox[0] + bbox[2] - max_text_width - self.margin, bbox[1] + bbox[3] + self.margin),
            'outside_left': (bbox[0] - max_text_width - self.margin, bbox[1] + (bbox[3] - total_text_height) // 2),
            'outside_right': (bbox[0] + bbox[2] + self.margin, bbox[1] + (bbox[3] - total_text_height) // 2)
        }

        # Get the starting position for the text
        x, y = positions.get(position, (self.margin, self.margin))

        # Intelligent switching to inside if the position is outside and doesn't fit within the image
        h, w, _ = self.image.shape
        if position.startswith('outside'):
            if x < 0 or x + max_text_width > w or y < 0 or y + total_text_height > h:
                # Switch to inside equivalent
                position = position.replace('outside', 'inside')
                x, y = positions.get(position, (self.margin, self.margin))

        # Draw the rounded rectangle background for the text
        self.draw_rounded_rectangle((x - self.bg_padding, y - self.bg_padding), (x + max_text_width, y + total_text_height), self.corner_radius, self.background_color, -1)

        # Add each line of text
        for i, (text, size) in enumerate(zip(texts, text_sizes)):
            initial_y_offset = self.bg_padding - (0.5 * self.bg_padding)
            text_y = y + initial_y_offset + i * (size[1] + self.padding)
            text_base_y = int(text_y + size[1])
            cv2.putText(self.image, text, (int(x), text_base_y), self.font, self.font_scale, self.font_color, self.thickness, self.line_type)
        
        return self.image
