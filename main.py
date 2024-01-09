import numpy as np
from PIL import Image, ImageOps
from flask import Flask, jsonify, render_template, request


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def hex_converter(file_path, code):
    my_image = Image.open(file_path).convert("RGB")
    size = my_image.size

    if size[0] >= 400 or size[1] >= 400:
        my_image = ImageOps.scale(image=my_image, factor=0.2)
    elif size[0] >= 600 or size[1] >= 600:
        my_image = ImageOps.scale(image=my_image, factor=0.4)
    elif size[0] >= 800 or size[1] >= 800:
        my_image = ImageOps.scale(image=my_image, factor=0.5)
    elif size[0] >= 1200 or size[1] >= 1200:
        my_image = ImageOps.scale(image=my_image, factor=0.6)
    my_image = ImageOps.posterize(my_image, 2)

    # Making a matrix of colours for our image
    image_array = np.array(my_image)

    # Creating a dictionary of unique colours
    unique_colours = {}
    for column in image_array:
        for rgb in column:
            t_rgb = tuple(rgb)
            if t_rgb not in unique_colours:
                unique_colours[t_rgb] = 0
            if t_rgb in unique_colours:
                unique_colours[t_rgb] += 1

    sorted_unique_colours = sorted(unique_colours.items(), key=lambda x: x[1], reverse=True)
    converted_dictionary = dict(sorted_unique_colours)
    # Get 10 highest values
    values = list(converted_dictionary.keys())
    top_10 = values[0:10]

    # Converting rgb to hex
    if code == "hex":
        hex_list = []
        for key in top_10:
            hex = rgb_to_hex(key)
            hex_list.append(hex)
        return hex_list
    else:
        return top_10


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image_file = request.files["file"]
        # reading the image file with stream property
        colour_code = request.form["colour_code"]
        colours = hex_converter(image_file.stream, colour_code)
        return render_template("index.html", colour_list=colours, code=colour_code)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
