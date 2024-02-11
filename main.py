from flask import Flask, request, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <form method="post" action="/upload" enctype="multipart/form-data">
        Height: <input type="text" name="height" placeholder="Height"><br>
        Width: <input type="text" name="width" placeholder="Width"><br>
        Image upload: <input type="file" name="image"><br>
        <input type="submit">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file uploaded', 400

    file = request.files['image']

    if not file.content_type.startswith('image/'):
        return 'File is not an image', 400

    if file.filename == '':
        return 'no selected file', 400

    if file:
        npimg = np.fromfile(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)

        width = int(request.form.get('width', 1024))
        height = int(request.form.get('height', 1024))

        resized_image = cv2.resize(img, (width, height))

        convert_status, buffer = cv2.imencode('.jpg', resized_image)

        if not convert_status:
            return 'Failed to convert image', 500

        temp_file = 'temp_image.jpg'
        cv2.imwrite(temp_file, resized_image)

        original_name = os.path.splitext(file.filename)[0]
        new_filename = f"{original_name}_{height}_{width}.jpg"

        return send_file(temp_file, download_name=new_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
