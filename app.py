from flask import Flask, request, jsonify, render_template
from PIL import Image
import os
import torch
from RealESRGAN import RealESRGAN

# Initialize Flask app
app = Flask(__name__)

# Initialize the Real-ESRGAN model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4.pth', download=True)

# Set upload and output directories
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/enhanced"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Home route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle image upload and enhancement
@app.route('/enhance', methods=['POST'])
def enhance_image():
    # Check if the request has a file
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the uploaded image
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_path)

    # Enhance the image using RealESRGAN
    try:
        image = Image.open(input_path).convert('RGB')
        enhanced_image = model.predict(image)

        # Save the enhanced image
        output_filename = f"enhanced_{file.filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        enhanced_image.save(output_path)

        # Return the file paths to the frontend
        return jsonify({
            'uploaded_image_url': f'/{input_path}',
            'enhanced_image_url': f'/{output_path}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
