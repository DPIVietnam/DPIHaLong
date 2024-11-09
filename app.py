from flask import Flask, render_template, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import os
import qrcode
import re

app = Flask(__name__)

# Lấy thông tin kết nối từ biến môi trường (Render cung cấp DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:jDByXhwpo3SUoZvnXxpp4m0hLzOeUQ5o@dpg-cskrmi3v2p9s73aah130-a.oregon-postgres.render.com/coasterdpi_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
id_CoasterDB = 654321
formatted_date = datetime.now().strftime("%Y.%m.%d")

def test_db_connection():
    try:
        # Thử kết nối tới cơ sở dữ liệu
        db.session.execute(text('SELECT 1'))  # Truy vấn đơn giản để kiểm tra kết nối
        print("Kết nối đến cơ sở dữ liệu PostgreSQL thành công!")
    except Exception as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")

class NumPhotosPrinted(db.Model):
    __tablename__ = 'numphotosprinted'  # Tên bảng
    id = db.Column(db.String(50), primary_key=True)  # Khóa chính
    quantity = db.Column(db.Integer)

@app.route('/')
def index():
    try:
        # test_db_connection()
        result = db.session.execute(text("SELECT to_regclass('public.numphotosprinted')"))
        table_exists = result.scalar()  # Dùng scalar() để lấy kết quả từ câu lệnh SQL
        
        if not table_exists:
            db.create_all()
        return render_template('index.html')
    except Exception as e:
        return f"Lỗi khi kiểm tra hoặc tạo bảng: {str(e)}" 

@app.route('/get_photos_printed', methods=['GET'])
def get_photos_printed():
    folder_path_pos1 = r'\\Coasterpos1\prints\Archive'
    folder_path_pos2 = r'\\Coasterpos2\prints\Archive'
    folder_path_pos3 = r'\\Coasterpos3\prints\Archive'

    path_pos1 = folder_path_pos1 + f'\\{formatted_date}\\s6x8'
    path_pos2 = folder_path_pos2 + f'\\{formatted_date}\\s6x8'
    path_pos3 = folder_path_pos3 + f'\\{formatted_date}\\s6x8'

    photos_printed_pos1 = get_count_files(path_pos1)
    photos_printed_pos2 = get_count_files(path_pos2)
    photos_printed_pos3 = get_count_files(path_pos3)
    
    today = datetime.now().strftime("%d.%m.%Y")
    file_count = 0
    if ((photos_printed_pos1 == 0 and photos_printed_pos2 == 0 and photos_printed_pos3 == 0) and not os.path.exists(folder_path_pos2)):
        result = db.session.execute(text("SELECT quantity FROM numphotosprinted WHERE id = :id"), {"id": id_CoasterDB})
        value = result.fetchone()
        print(value)
        file_count = value[0]
    else:
        file_count = photos_printed_pos1 + photos_printed_pos2 + photos_printed_pos3
        try:
            db.session.execute(text("UPDATE numphotosprinted SET quantity = :quantity WHERE id = :id"), {"quantity": file_count, "id": id_CoasterDB})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Lỗi: {e}")

    return jsonify({'today': today, 'file_count': file_count}) 

def get_count_files(folder_path):
    try:
        return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    except Exception as e:
        return 0
    
@app.route('/show_qrcode', methods=['POST'])
def show_qrcode():
    urlExample = 'https://sharepix.com.au/ht/uploads/'
    numQr = request.json.get('numQr')

    folder_path_pos1 = r'\\Coasterpos1\prints\Archive'
    folder_path_pos2 = r'\\Coasterpos2\prints\Archive'
    folder_path_pos3 = r'\\Coasterpos3\prints\Archive'

    path_pos1 = folder_path_pos1 + f'\\{formatted_date}\\s6x8'
    path_pos2 = folder_path_pos2 + f'\\{formatted_date}\\s6x8'
    path_pos3 = folder_path_pos3 + f'\\{formatted_date}\\s6x8'

    file_pattern = re.compile(r'\d{3}-\w{3}-' + re.escape(str(numQr)) + r'\.jpg')

    def search_in_folder(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                print(file)
                if file_pattern.match(file):  # Kiểm tra nếu tên file khớp với pattern
                    return file  # Trả về tên file, không phải đường dẫn

        return None  # Nếu không tìm thấy tệp nào khớp

    url = ''
    for path in [path_pos1, path_pos2, path_pos3]:
        print(path)
        result = search_in_folder(path)
        print(result)
        if result:
            url = urlExample + result
            break

    if url == '':
        return jsonify({'result': False})

    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Lưu hình ảnh vào thư mục /images
    image_path = os.path.join('static/images', 'qrcode.png')  # Đặt đường dẫn lưu tệp

    # Kiểm tra thư mục images có tồn tại không, nếu không thì tạo mới
    if not os.path.exists('images'):
        os.makedirs('images')

    # Lưu hình ảnh vào tệp
    img.save(image_path, 'PNG')

    return jsonify({'result': True, 'path': image_path})
    

if __name__ == '__main__':
    app.run(debug=True)
