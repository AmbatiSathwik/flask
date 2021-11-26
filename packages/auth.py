from flask import Blueprint, g, render_template, request, flash, redirect, url_for
import psycopg2
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = db.get_db()
        cur = conn.cursor()
        userid = request.form.get('usrid')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('pass')
        is_admin = False
        
        cur.execute(
            "select (id) from usr where id=%s", (userid,))
        ee = cur.fetchall()
        if ee:
            flash('Userid already exists', category='error')
            return redirect(url_for('auth.signup'))
        
        if not (userid and email):
            flash('Enter all feilds.', category='error')
            return redirect(url_for('auth.signup'))
        else:
            flash('Account created successfully, you can login now',
                  category='success')

            cur.execute('insert into usr(id,email,password,phone,is_admin) values (%s,%s,%s,%s,%s)',
                        (userid, email, password, phone,is_admin))
            conn.commit()
            cur.close()
            return redirect("/signup")
    return render_template("signup.html")

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        conn = db.get_db()
        cur = conn.cursor()
        userid = request.form.get('usrid')
        password = request.form.get('pass')
        print(password)
        cur.execute(
            "select (password) from usr where id = %s", (userid,))
        passi = cur.fetchall()
        if not passi:
            flash('No username found, try signup', category='error')
            return redirect(url_for('auth.signup'))
        for p in passi:
            if password == p[0]:
                cur.execute(
                    "select (is_admin) from usr where id = %s", (userid,))
                adm = cur.fetchall()
                for a in adm:
                    if a[0]:
                        print("admin")
                        return redirect("/signin")
                    else:
                        print("user")
                        return redirect("/signin")
            else:
                flash('Password not correct.', category='error')
                return redirect(url_for('auth.signin'))
        cur.close()
    return render_template("login.html")