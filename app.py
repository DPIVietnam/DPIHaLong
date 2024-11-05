from flask import Flask, render_template, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import os

app = Flask(__name__)

# Lấy thông tin kết nối từ biến môi trường (Render cung cấp DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:jDByXhwpo3SUoZvnXxpp4m0hLzOeUQ5o@dpg-cskrmi3v2p9s73aah130-a.oregon-postgres.render.com/coasterdpi_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
id_CoasterDB = 654321

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
    formatted_date = datetime.now().strftime("%Y.%m.%d")

    folder_path_pos1 = r'\\Coasterpos1\prints\Archive'
    folder_path_pos2 = r'\\Coasterpos2\prints\Archive'
    folder_path_pos3 = r'\\Coasterpos3\prints\Archive'

    path_pos1 = folder_path_pos1 + f'\\{formatted_date}\\s6x8'
    path_pos2 = folder_path_pos2 + f'\\{formatted_date}\\s6x8'
    path_pos3 = folder_path_pos3 + f'\\{formatted_date}\\s6x8'

    photos_printed_pos1 = get_count_files(path_pos1)
    photos_printed_pos2 = get_count_files(path_pos2)
    photos_printed_pos3 = get_count_files(path_pos3)

    file_count = 0
    if (photos_printed_pos1 == -1 | photos_printed_pos2 == -1 | photos_printed_pos3 == -1):
        result = db.session.execute(text("SELECT quantity FROM numphotosprinted WHERE id = :id"), {"id": id_CoasterDB})
        value = result.fetchone()
        print(value[0])
        file_count = value[0]
    else:
        file_count = photos_printed_pos1 + photos_printed_pos2 + photos_printed_pos3
        try:
            db.session.execute(text("UPDATE numphotosprinted SET quantity = :quantity WHERE id = :id"), {"quantity": file_count, "id": id_CoasterDB})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Lỗi: {e}")
    
    return jsonify({'file_count': file_count}) 

def get_count_files(folder_path):
    try:
        return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    except Exception as e:
        return -1

if __name__ == '__main__':
    app.run(debug=True)
