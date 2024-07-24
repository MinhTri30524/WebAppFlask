from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os


app = Flask(__name__)
#bao mat
app.config["SECRET_KEY"] = "tri"
app.permanent_session_lifetime = timedelta(minutes=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    svname = db.Column(db.String(100), nullable=False)
    mssv = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<Student {self.svname}>'
def init_db():
    with app.app_context():
        db.create_all()
        
        print("Các bảng cơ sở dữ liệu đã được tạo.")

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/thongtin", methods=["POST", "GET"])
def thongtin():
    if request.method == "POST":
        tensinhvien = request.form["svname"]
        masosinhvien = request.form["mssv"]

        existing = Student.query.filter_by(mssv=masosinhvien).first()
        if existing:
            flash('Mã số sinh viên đã tồn tại !!!', 'error')
        else:
            db_new = Student(svname=tensinhvien, mssv=masosinhvien)
            db.session.add(db_new)
            db.session.commit()
            flash('Sinh viên đã được thêm thành công!!', 'success')

        return redirect(url_for('thongtin'))
    
    db_all = Student.query.all() #Lấy tất cả sinh viên để hiển thị
    return render_template('thongtin.html', students=db_all)

@app.route("/diemdanh")
def diemdanh():
    db_all = Student.query.all()  # Lấy tất cả sinh viên để hiển thị
    return render_template('diemdanh.html', students=db_all)

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        password = request.form["password"]
        if user_name and password == "admin":
            session.permanent = True
            session["user"] = user_name
            flash("You Logged in successfully!!!", "info")
            return render_template("user.html", user=user_name)
        else:
            flash("Invalid credentials! Please try again.", "danger")
            return redirect(url_for("login"))
    if "user" in session:
        name = session["user"]
        flash("You have already logged in!!!", "info")
        return render_template("user.html", user=name)
    return render_template('login.html')



@app.route("/user")
def hello_user():
    if "user" in session:
        name = session["user"]
        return render_template("user.html", user=name)
    else:
        flash("You are not logged in!!!", "info")
        return redirect(url_for("login"))
    
@app.route("/logout")
def log_out():
    flash("You Logged Out!!!", "info")
    session.pop("user", None)
    return redirect(url_for("home"))



if __name__ == '__main__':
    init_db()
    app.run(debug = True)