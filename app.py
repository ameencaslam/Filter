from flask import Flask, render_template, jsonify, request, send_from_directory
import pandas as pd
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BATCH_SIZE = 72
FAKE_CSV = 'data/fake.csv'
REAL_CSV = 'data/real.csv'

# Replace before_first_request with a function that runs at startup
def check_paths():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    fake_dir = os.path.join(base_dir, 'data', 'fake')
    real_dir = os.path.join(base_dir, 'data', 'real')
    
    logger.debug(f"Base directory: {base_dir}")
    logger.debug(f"Fake images directory: {fake_dir}")
    logger.debug(f"Real images directory: {real_dir}")
    
    logger.debug(f"Fake directory exists: {os.path.exists(fake_dir)}")
    logger.debug(f"Real directory exists: {os.path.exists(real_dir)}")

# Call check_paths at startup
check_paths()

def initialize_csv(folder_path, csv_path):
    if not os.path.exists(csv_path):
        # Get all image files from the folder
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        df = pd.DataFrame({
            'filename': images,
            'status': ['original'] * len(images)
        })
        df.to_csv(csv_path, index=False)

def get_batch(csv_path):
    df = pd.read_csv(csv_path)
    original_images = df[df['status'] == 'original']['filename'].tolist()
    batch = original_images[:BATCH_SIZE]
    
    stats = {
        'original': len(df[df['status'] == 'original']),
        'true': len(df[df['status'] == 'true']),
        'false': len(df[df['status'] == 'false'])
    }
    
    return batch, stats

@app.route('/')
def index():
    # Initialize CSVs if they don't exist
    initialize_csv('data/fake', FAKE_CSV)
    initialize_csv('data/real', REAL_CSV)
    return render_template('index.html')

@app.route('/get_batch')
def get_next_batch():
    dataset = request.args.get('dataset', 'fake')
    csv_path = FAKE_CSV if dataset == 'fake' else REAL_CSV
    folder_path = 'data/fake' if dataset == 'fake' else 'data/real'
    
    # Use OS-agnostic path separator
    folder_path = folder_path.replace('/', os.path.sep)
    
    batch, stats = get_batch(csv_path)
    # Use forward slashes for URLs even on Windows
    return jsonify({
        'images': [f'{folder_path}/{img}'.replace('\\', '/') for img in batch],
        'stats': stats
    })

@app.route('/update_batch', methods=['POST'])
def update_batch():
    data = request.json
    dataset = data.get('dataset', 'fake')
    true_images = data.get('true_images', [])
    false_images = data.get('false_images', [])
    
    csv_path = FAKE_CSV if dataset == 'fake' else REAL_CSV
    df = pd.read_csv(csv_path)
    
    # Update statuses
    df.loc[df['filename'].isin(true_images), 'status'] = 'true'
    df.loc[df['filename'].isin(false_images), 'status'] = 'false'
    
    df.to_csv(csv_path, index=False)
    
    # Get next batch and stats
    batch, stats = get_batch(csv_path)
    return jsonify({
        'success': True,
        'stats': stats
    })

@app.route('/<path:filename>')
def serve_image(filename):
    logger.debug(f"Attempting to serve image: {filename}")
    
    # Get the absolute path to your project directory
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Construct the full path
    full_path = os.path.join(base_dir, filename)
    logger.debug(f"Full path: {full_path}")
    
    # Get directory and filename
    directory = os.path.dirname(full_path)
    file_name = os.path.basename(full_path)
    
    if os.path.exists(full_path):
        logger.debug(f"File found: {full_path}")
        return send_from_directory(directory, file_name)
    else:
        logger.error(f"File not found: {full_path}")
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True) 