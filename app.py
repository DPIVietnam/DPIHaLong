from flask import Flask, render_template, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
# from shutil import copyfile
# from PIL import Image
# import cv2
# from skimage import exposure
import numpy as np

import os
# import qrcode
# import re
# import shutil

app = Flask(__name__)

# Lấy thông tin kết nối từ biến môi trường (Render cung cấp DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:Qj5PUtYJ4Rf5GbeGGzpljyVq3pmeoDQk@dpg-d2r99s56ubrc73ecrh5g-a.singapore-postgres.render.com/coasterdpi15_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
id_CoasterDB = '654321'
id_HtDB = '999999'
now = datetime.now()
formatted_date = now.strftime("%Y.%m.%d")

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

class NumPhotosPrintedHt(db.Model):
    __tablename__ = 'numphotosprintedht'  # Tên bảng
    id = db.Column(db.String(50), primary_key=True)  # Khóa chính
    standard = db.Column(db.Integer)
    full = db.Column(db.Integer)
    extra = db.Column(db.Integer)
    customer = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    quantity_backup = db.Column(db.Integer)

@app.route('/')
def index():
    try:
        test_db_connection()
        # delete = db.session.execute(text("DELETE FROM numphotosprintedht WHERE id = :id"), {'id': '123456'})
        # db.session.commit()
        result = db.session.execute(text("SELECT to_regclass('public.numphotosprintedht')"))
        table_exists = result.scalar()  # Dùng scalar() để lấy kết quả từ câu lệnh SQL
        
        
        if not table_exists:
            db.create_all()
            print('Database created successfull')
        else:
            print('nnn')
        return render_template('index.html')
    except Exception as e:
        return f"Lỗi khi kiểm tra hoặc tạo bảng: {str(e)}" 

@app.route('/get_photos_printed', methods=['GET'])
def get_photos_printed():
    # db.session.execute(text("INSERT INTO numphotosprinted VALUES (:id, :quantity)"), {"id": id_CoasterDB, "quantity": 0})
    # db.session.commit()
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
    print(today)
    file_count = 0
    if ((photos_printed_pos1 == 0 and photos_printed_pos2 == 0 and photos_printed_pos3 == 0) and not os.path.exists(folder_path_pos2)):
        result = db.session.execute(text("SELECT quantity FROM numphotosprinted WHERE id = :id"), {"id": id_CoasterDB})
        value = result.fetchone()
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

def get_count_folder(folder_path):
    try:
        return len([name for name in os.listdir(folder_path)])
    except Exception as e:
        return 0
    
@app.route('/get_photos_printed_ht', methods=['GET'])
def get_photos_printed_ht():
    date_now = now.strftime("%Y_%m_%d")
    target_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    path_ops = r"C:\CapImages\Ops"
    customer_path = r"C:\Customers"
    photo_standard = 0
    photo_extra = 0
    photo_full = 0
    photo_customer = get_count_folder(customer_path)
    try:
        for file_name in os.listdir(path_ops):
            if file_name.startswith(date_now) and file_name.endswith('_Log.txt'):
                duong_dan_file = os.path.join(path_ops, file_name)

                with open(duong_dan_file, 'r') as file:
                    lines = file.readlines()

                    # Lặp qua từng dòng để tính tổng tiền
                    for line in lines:
                        # Tách thông tin từ dòng
                        thong_tin = line.strip().split(', ')

                        # Lấy giá trị từ cột thứ 6 (số tiền)
                        so_tien = int(thong_tin[5])

                        # Lấy loại gói từ cột thứ 1
                        loai_goi = thong_tin[1]

                        # Tính tổng tiền dựa trên loại gói
                        if "Standard" in loai_goi:
                            photo_standard += 1
                        elif "Extra" in loai_goi:
                            photo_extra += 1
                        elif "Full" in loai_goi:
                            photo_full += 1
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi: {e}")
        
    folder_path_pos1 = f"C:\\prints\\Archive"
    folder_path_pos2 = f"\\DPIPrintserver2\\prints\\Archive"

    path_pos1 = folder_path_pos1 + f'\\{formatted_date}\\s8x10'
    path_pos2 = folder_path_pos2 + f'\\{formatted_date}\\s8x10'

    photos_printed_pos1 = get_count_files(path_pos1)
    photos_printed_pos2 = get_count_files(path_pos2)


    file_stand = 0
    file_full = 0
    file_extra = 0
    file_customer = 0
    file_count = 0
    # db.session.execute(text("INSERT INTO numphotosprintedht VALUES (:id, :standard, :full, :extra, :customer, :quantity, :quantity_backup)"), {"id": id_HtDB ,"standard": 0, "full": 0, "extra": 0, "customer": 0, "quantity": 0, "quantity_backup": 0})
    # db.session.commit()

    result = db.session.execute(text("SELECT * FROM numphotosprintedht WHERE id = :id"), {"id": id_HtDB})
    value = result.fetchone()

    print(value)

    if (photos_printed_pos1 == 0 and photos_printed_pos2 == 0 and not os.path.exists(folder_path_pos1)):
        file_stand = value[1]
        file_full = value[2]
        file_extra = value[3]
        file_customer = value[4]
        file_count = value[5]
    else:
        if now > target_time and os.path.exists(folder_path_pos1) and not os.path.exists(folder_path_pos2):
            file_count = photos_printed_pos1 + value[5]
        else:
            file_count = photos_printed_pos1 + photos_printed_pos2
        file_stand = photo_standard
        file_full = photo_full
        file_extra = photo_extra
        file_customer = photo_customer
        try:
            db.session.execute(text("""UPDATE numphotosprintedht SET standard = :standard, "full" = :photo_full, extra = :extra, customer = :customer, quantity = :quantity, quantity_backup = :quantity_backup WHERE id = :id"""),
                            {"standard": photo_standard, "photo_full": photo_full, "extra": photo_extra, "customer": file_customer, "quantity": file_count, "quantity_backup": photos_printed_pos2, "id": id_HtDB})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Lỗi: {e}")

    return jsonify({'file_stand': file_stand, 'file_full': file_full, 'file_extra': file_extra, 'file_customer': file_customer, 'file_count': file_count}) 

if __name__ == '__main__':
    app.run(debug=True)
