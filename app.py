from flask import Flask, render_template, request, jsonify, send_file, redirect, session
import csv
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "attendance_secret_key"


# ADMIN LOGIN DETAILS
ADMIN_USER = "deebu"
ADMIN_PASS = "1234"


# Login Page
@app.route("/")
def login():
    return render_template("login.html")


# Login Check
@app.route("/login",methods=["POST"])
def login_check():

    username=request.form["username"]
    password=request.form["password"]

    if username==ADMIN_USER and password==ADMIN_PASS:

        session["admin"]=True
        return redirect("/home")

    return "Wrong Username or Password"


# Home Page
@app.route("/home")
def home():

    if "admin" not in session:
        return redirect("/")

    return render_template("home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Register Page
@app.route("/register_page")
def register_page():

    if "admin" not in session:
        return redirect("/")

    return render_template("register.html")


# Attendance Page
@app.route("/attendance_page")
def attendance_page():

    if "admin" not in session:
        return redirect("/")

    return render_template("attendance.html")


@app.route("/view_attendance")
def view_attendance():

    if "admin" not in session:
        return redirect("/")

    return render_template("view_attendance.html")


@app.route("/percentage_page")
def percentage_page():

    if "admin" not in session:
        return redirect("/")

    return render_template("percentage.html")


# REGISTER STUDENT
@app.route("/register_student", methods=["POST"])
def register_student():

    data=request.get_json()

    name=data["name"]
    roll=data["roll"]

    file_exists=os.path.exists("students.csv")

    with open("students.csv","a",newline="") as f:

        writer=csv.writer(f)

        if not file_exists:
            writer.writerow(["Name","Roll"])

        writer.writerow([name,roll])

    return jsonify({"message":"Student Registered"})


# GET STUDENTS
@app.route("/get_students")
def get_students():

    students=[]

    if os.path.exists("students.csv"):

        with open("students.csv","r") as f:

            reader=csv.reader(f)
            next(reader,None)

            for row in reader:
                students.append(row)

    return jsonify({"students":students})


# SAVE ATTENDANCE
@app.route("/save_attendance",methods=["POST"])
def save_attendance():

    data=request.get_json()

    names=data["names"]

    today=datetime.now().strftime("%Y-%m-%d")

    file_exists=os.path.exists("attendance.csv")

    with open("attendance.csv","a",newline="") as f:

        writer=csv.writer(f)

        if not file_exists:
            writer.writerow(["Name","Status","Date"])

        for name in names:
            writer.writerow([name,"Present",today])

    return jsonify({"message":"Attendance Saved"})


# GET ATTENDANCE
@app.route("/get_attendance")
def get_attendance():

    view_type=request.args.get("type")

    data=[]

    today=datetime.now().strftime("%Y-%m-%d")

    if os.path.exists("attendance.csv"):

        with open("attendance.csv","r") as f:

            reader=csv.reader(f)
            next(reader,None)

            for row in reader:

                if view_type=="today":

                    if row[2]==today:
                        data.append(row)

                else:
                    data.append(row)

    return jsonify({"attendance":data})


# DOWNLOAD CSV
@app.route("/download_csv")
def download_csv():

    if os.path.exists("attendance.csv"):
        return send_file("attendance.csv",as_attachment=True)

    return "No File"





