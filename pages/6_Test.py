import base64
from PIL import Image
import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

import base64
from PIL import Image
from io import BytesIO

def load_and_combine_images(filename1, filename2, folder1, folder2):
    # Open first image
    with open("./{}/{}.jpg".format(folder1.lower(), filename1.lower()), "rb") as f1:

        image1 = Image.open(f1)

        # Open second image
        with open("./{}/{}.jpg".format(folder2.lower(), filename2.lower()), "rb") as f2:

            image2 = Image.open(f2)

            # Ensure both images have the same size
            width, height = 800,592
            try:
                image1 = image1.crop((width, height))
            except:
                image1 = image1.resize((width, height))

            try:
                image2 = image2.crop((width, height))
            except:
                image2 = image2.resize((width, height))

        
            # Create a new blank image
            combined_image = Image.new('RGB', (width, height))

            # Combine the images along the diagonal
            for x in range(width):
                for y in range(height):
                    if x + y <= height:  # Cut along the diagonal
                        pixel = image1.getpixel((x, y))
                    else:
                        pixel = image2.getpixel((x, y))

                    combined_image.putpixel((x, y), pixel)

            # Convert the combined image to base64
            buffered = BytesIO()
            combined_image.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return "data:image/jpeg;base64," + encoded_image

# Ejemplo de uso:
filename1 = "keznit"
filename2 = "aspas"
folder1 = "players"
folder2 = "players"

imagen_combinada = load_and_combine_images(filename1, filename2, folder1, folder2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True): 
        a = card(
                title = "aaaa",
                text = "prueba",
                image = imagen_combinada,
                styles={
                    "card": {
                        "width": "100%",
                        "height": "400px"
                            }
                        }
                                    )