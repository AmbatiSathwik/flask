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
        #print(password)
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
                        #print("admin")
                        return redirect("/admin") #admin page
                    else:
                        #("user")
                        return redirect(url_for("auth.user", user=userid))
            else:
                flash('Password not correct.', category='error')
                return redirect(url_for('auth.signin'))
        cur.close()
    return render_template("login.html")

@auth.route("/<user>", methods=['GET', 'POST'])
def user(user):
    if request.method == "GET":
        ret = [user,0,0,0]
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute(
            "select (rid) from resident where sid = %s", (user,)
        )
        roomnum = cur.fetchall()
        if roomnum:
            room = False
            ret[1] = roomnum[0][0]
            cur.execute(
                "select (hid) from room where id = %s", (roomnum[0],)
            )
            hosnum = cur.fetchall()
            ret[2] = hosnum[0][0]
            ret[3] = roomnum[0][0][1]
        else:
            room = True
        cur.close()
        return render_template("student.html",room=room,ret=ret)
    if request.method == "POST":
        check = request.form.get("rname")
        if check:
            #request room
            name = request.form.get("rname")
            sid = request.form.get("rroll")
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute(
                'insert into complient(Ctype,description,sid) values (%s,%s,%s)', ("room",name,sid)
            )
            conn.commit()
            cur.close()
            flash('Room Request registered successfully.', category='success')
            return redirect(url_for("auth.user", user=user))
        else:
            #complaint
            rid = request.form.get("rid")
            name = request.form.get("cname")
            sid = request.form.get("croll")
            hid = rid[0]
            typ = request.form.get("select")
            des = request.form.get("message")
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute(
                'insert into complient(Ctype,description,sid,rid,hid) values (%s,%s,%s,%s,%s)', (typ,des,sid,rid,hid)
            )
            conn.commit()
            cur.close()
            flash('Complaint registered successfully.', category='success')
            return redirect(url_for("auth.user", user=user))
        return redirect(f"/{user}")

@auth.route("/admin")
def admin():
    room_det = []
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(
        'select (description,sid) from complient where Ctype = %s', ("room",)
    )
    room = cur.fetchall()
    for r in room:
        det = [None,None]
        name,sid = r[0].split(",")
        det[0] = name[1:]
        det[1] = sid[:-1]
        room_det.append(det)
        
    compliants = []
    cur.execute(
        'select (Ctype,description,rid,hid,Cno) from complient where Ctype != %s', ("room",)
    )
    com = cur.fetchall()
    for c in com:
        comp = [None,None,None,None,None]
        Ctype,description,rid,hid,cno = c[0].split(",")
        comp[0] = Ctype[2:-1]
        comp[1] = description[1:-1]
        comp[2] = rid
        comp[3] = hid
        comp[4] = cno[:-1]
        compliants.append(comp)
    cur.close()
    return render_template("admin.html",room_det=room_det,compliants=compliants)

def allocate():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(
        'select * from room',
    )
    room = cur.fetchall()
    #print(room)
    for r in room:
        id,vacancy,capacity,hid = r
        vacancy = int(vacancy)
        capacity = int(capacity)
        if vacancy:
            cur.close()
            return id
    cur.close()
    return False
    
@auth.route("/reject/<user>", methods=["POST"])
def reject(user):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("delete from complient where sid=%s and Ctype=%s",(user,"room",))
    conn.commit()
    cur.close()
    return "REJECTED"

@auth.route("/approve/<user>", methods=["POST"])
def approve(user):
    room = allocate()
    if not room:
        return False
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select vacancy from room where id=%s",(room,))
    vac = cur.fetchall()
    vac = vac[0][0] - 1
    cur.execute("update room set vacancy=%s where id=%s",(vac,room,))
    cur.execute("insert into resident(sid,rid) values (%s,%s)",(user,room,))
    cur.execute("delete from complient where sid=%s and Ctype=%s",(user,"room",))
    conn.commit()
    cur.close()
    return room

@auth.route("/done/<cno>", methods=["POST"])
def done(cno):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("delete from complient where Cno=%s",(cno,))
    conn.commit()
    cur.close()
    return "complient done"
