from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from . import db
from .models import Contact
from sqlalchemy import text  

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/contact", methods=["GET", "POST"])
def contact():
    full_name = request.form.get('fullName')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not full_name or not email or not subject or not message:
        flash("Please fill out all fields!", "danger")
        return redirect(url_for('main.home'))

    # บันทึกลง database
    new_contact = Contact(
        full_name=full_name,
        email=email,
        subject=subject,
        message=message
    )
    db.session.add(new_contact)
    db.session.commit()

    flash("Your message has been sent successfully!", "success")
    return redirect(url_for('main.home'))
    
@main.route("/test-db")
def test_db():
    try:
        # ใช้ text() แปลง SQL string ให้ executable
        result = db.session.execute(text("SELECT 1"))
        value = result.scalar()  # ดึงค่า
        return jsonify({"status": "ok", "value": value})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})