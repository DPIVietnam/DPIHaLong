from flask import Flask, render_template, request, jsonify

import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_photos_printed', methods=['GET'])
def get_photos_printed():
    folder_path_pos1 = r'\\Coasterpos2\prints\Archive\2024.11.04\s6x8'
    folder_path_pos2 = r'\\Coasterpos2\prints\Archive\2024.11.04\s6x8'
    folder_path_pos3 = r'\\Coasterpos2\prints\Archive\2024.11.04\s6x8'

    photos_printed_pos1 = get_count_files(folder_path_pos1)
    photos_printed_pos2 = get_count_files(folder_path_pos2)
    photos_printed_pos3 = get_count_files(folder_path_pos3)

    if (photos_printed_pos1 == -1 | photos_printed_pos2 == -1 | photos_printed_pos3 == -1):
        return jsonify({'error': 'Folder path not found!'})
    else:
        file_count = photos_printed_pos1 + photos_printed_pos2 + photos_printed_pos3
        return jsonify({'file_count': file_count}) 

def get_count_files(folder_path):
    try:
        return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    except Exception as e:
        return -1

if __name__ == '__main__':
    app.run(debug=True)
