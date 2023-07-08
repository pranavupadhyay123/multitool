import os
import io
import base64
import secrets
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from PIL import Image

app = Flask(__name__)
app.secret_key = 'hfPDJsGiYy0nB9ZC'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get uploaded image from the form
        uploaded_image = request.files['image']

        # Open the image using PIL
        img = Image.open(uploaded_image)

        # Convert the image to RGB mode
        img = img.convert('RGB')

        # Resize the image
        width = int(request.form['width'])
        height = int(request.form['height'])
        resized_img = img.resize((width, height))

        # Generate a unique filename for the resized image
        filename = secrets.token_hex(8) + '.jpg'
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

        # Save the resized image to the download folder
        resized_img.save(filepath, 'JPEG')

        return redirect(url_for('download', filename=filename))

    return render_template('index.html')


@app.route('/download/<filename>')
def download(filename):
    # Retrieve the file path based on the filename
    filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

    # Check if the file exists
    if not os.path.isfile(filepath):
        return redirect(url_for('index'))

    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
