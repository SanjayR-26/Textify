# Textify
 Textify is a lightweight and powerful Python tool for overlaying customizable text on images. With support for dynamic positioning, rounded bounding boxes, and intelligent space adaptation, Textify ensures that your annotations are always clear and visually appealing. Perfect for object detection, image annotation, and more!

--------------------------------------------------

## Overview

The `TextOverlay` class is a versatile Python utility that allows you to overlay text onto an image, with support for customizable properties such as font scale, color, thickness, background color, and more. It also includes the ability to draw bounding boxes with rounded corners and intelligently position text within or outside the bounding box, adapting to the available space in the image.

## Features

### 1. **Customizable Text Properties**
   - **Font Scale**: Adjust the size of the text for better visibility.
   - **Font Color**: Specify the color of the text in (B, G, R) format.
   - **Thickness**: Set the thickness of the text for different levels of emphasis.
   - **Background Color**: Define the background color for the text block to ensure readability against any image.

### 2. **Bounding Box with Rounded Corners**
   - The class allows you to draw a bounding box around a specific area of the image.
   - Rounded corners provide a polished, modern look.
   - You can customize the corner radius, thickness, and color of the bounding box.

### 3. **Text Positioning Options**
   - **Flexible Positioning**: The text can be positioned in various locations relative to the bounding box or the entire image. Options include:
     - Inside: top-left, top-center, top-right, bottom-left, bottom-center, bottom-right.
     - Outside: top-left, top-center, top-right, bottom-left, bottom-center, bottom-right, left, and right.
   - **Intelligent Positioning**: If the chosen position doesn't fit within the image boundaries, the class automatically switches to an inside position to ensure the text remains visible.

### 4. **Automatic Adaptation**
   - The `TextOverlay` class automatically adapts the text position to fit within the image if there's limited space, ensuring that your text is always legible.

### 5. **Background and Padding**
   - You can set a background color for the text to improve readability against various image backgrounds.
   - The class includes padding around the text block and within the background box, ensuring the text doesn't touch the edges and is well spaced.

### 6. **Versatile Usage**
   - Ideal for applications in object detection, face recognition, image annotation, or any scenario where you need to overlay text on images with precise control over appearance and positioning.

## How to Use

### Initialization

```python
image = cv2.imread('path_to_your_image.jpg')
overlay = TextOverlay(image)
```

### Setting Text Properties

```python
overlay.set_text_properties(
    font_scale=1.0,
    font_color=(0, 0, 0),  # Black text
    thickness=2,
    background_color=(255, 255, 255)  # White background
)
```

### Adding Text with Bounding Box

```python
texts = ['Face recognized', 'Confidence: 99%']
bbox = [600, 500, 700, 700]  # [x, y, width, height]

modified_image = overlay.put_text(
    texts,
    bbox=bbox,
    position='outside_top_center',
    bbox_color=(0, 255, 0)  # Green bounding box
)
```

### Displaying the Modified Image

```python
cv2.imshow('Modified Image', modified_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Auto-Adaptation Example

If the position you choose doesn't fit within the image boundaries, the class will automatically adjust the text position to ensure it stays visible within the image.

### Drawing Bounding Box with Rounded Corners

```python
overlay.draw_bbox(
    bbox=[600, 500, 700, 700],
    color=(0, 255, 0),  # Green bounding box
    thickness=2
)
```

## Conclusion

The `TextOverlay` class is a powerful tool for adding text overlays to images in a flexible and customizable manner. With its intelligent positioning and auto-adaptation features, it ensures that your text annotations are always clear and visible, regardless of the image's dimensions or content.

Feel free to explore and modify the parameters to best suit your application needs!
