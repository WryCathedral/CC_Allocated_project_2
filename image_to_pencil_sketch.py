import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk


def convert_to_pencil_sketch():
    global image_path, original_image_pil

    if image_path:
        # Read the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert the grayscale image
        inverted_image = cv2.bitwise_not(gray_image)

        # Blur the inverted image using GaussianBlur
        blurred_image = cv2.GaussianBlur(inverted_image, (111, 111), 0)

        # Invert the blurred image
        inverted_blurred_image = cv2.bitwise_not(blurred_image)

        # Create the pencil sketch by blending the grayscale image with the inverted blurred image
        pencil_sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        # Convert the sketch image to PIL format for displaying in Tkinter
        sketch_image_pil = Image.fromarray(pencil_sketch)

        # Resize the images to fit the window
        sketch_image_pil = sketch_image_pil.resize((400, 400))

        # Update the images in the Tkinter labels
        sketch_image_tk = ImageTk.PhotoImage(sketch_image_pil)
        sketch_image_label.config(image=sketch_image_tk)
        sketch_image_label.image = sketch_image_tk


def open_file_dialog():
    global image_path, original_image_pil

    # Open file dialog to choose an image file
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path = file_path

        # Load the original image and store it as a PIL image
        original_image = Image.open(image_path)
        original_image = original_image.resize((400, 400))
        original_image_pil = ImageTk.PhotoImage(original_image)

        # Update the original image label
        original_image_label.config(image=original_image_pil)
        original_image_label.image = original_image_pil

        # Convert the image to a pencil sketch
        convert_to_pencil_sketch()


def exit_program():
    root.destroy()


# Create the main application window
root = tk.Tk()
root.title("Image to Pencil Sketch Converter")

# Create the button for opening the file dialog
open_button = tk.Button(root, text="Open Image", command=open_file_dialog)
open_button.grid(row=0, column=0, pady=10)

# Create labels for displaying the images
original_label = tk.Label(root, text="Original Image")
original_label.grid(row=1, column=0)
original_image_label = tk.Label(root)
original_image_label.grid(row=2, column=0, padx=10, pady=10)

sketch_label = tk.Label(root, text="Pencil Sketch")
sketch_label.grid(row=1, column=1)
sketch_image_label = tk.Label(root)
sketch_image_label.grid(row=2, column=1, padx=10, pady=10)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.grid(row=3, column=0, columnspan=2, pady=10)

# Variables to store the selected image path and the original image
image_path = None
original_image_pil = None

# Run the application
root.mainloop()
