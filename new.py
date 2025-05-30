from flask import Flask, render_template, request, redirect, url_for
import mysql.connector



app = Flask(__name__)
app.config["SECRET_KEY"] = "phucdz"


#Kết nối Mysql
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alanphuc1609@",
    database="sinhvien"
)
cursor = conn.cursor()


#Trang Home
@app.route('/')
def home():
    return render_template("home.html")


#Trang Bảng
@app.route('/form')
def form():
    cursor.execute("SELECT * FROM sv")
    data = cursor.fetchall()
    cursor.execute("SHOW COLUMNS FROM sv")
    columns = [col[0] for col in cursor.fetchall()]
    return render_template('index.html', data=data, columns=columns)


#Thêm sinh viên
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        msv = request.form['msv']
        ten = request.form['ten']
        ngaysinh = request.form['ngaysinh']
        lop = request.form['lop']
        diem = request.form['diem']
        from datetime import datetime
        try:
            ngaysinh = datetime.strptime(ngaysinh, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return "Ngày sinh không hợp lệ", 400

        sql = "INSERT INTO sv (MSV, `Tên`, `Ngày Sinh`, `Lớp`, `Điểm`) VALUES (%s, %s, %s, %s, %s)"
        values = (msv, ten, ngaysinh, lop, diem)
        cursor.execute(sql, values)
        conn.commit()
        return redirect(url_for('form'))
    else:
        return render_template('add.html')
    

#Xóa sinh viên
@app.route('/delete/<msv>', methods=['POST'])
def delete(msv):
    sql = "DELETE FROM sv WHERE msv = %s"
    values = (msv,)
    cursor.execute(sql, values)
    conn.commit()
    return redirect(url_for('form'))



if __name__ == '__main__':
    app.run(debug=True)
