from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = 'C:/karthik/RFP/Upload'

# Route to accept file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the upload folder
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Return the filename and the path where the file is saved
    return jsonify({'filename': file.filename, 'file_path': filename}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
