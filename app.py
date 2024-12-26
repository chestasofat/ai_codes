from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_image', methods=['POST'])
def get_image():
    animal = request.form.get('animal')
    if animal in ['cat', 'dog', 'elephant']:
        image_url = f"/static/images/{animal}.jpg"
        return jsonify({'image_url': image_url})
    return jsonify({'error': 'Invalid selection'}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    response = {
        'name': filename,
        'size': os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)),
        'type': file.content_type
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
