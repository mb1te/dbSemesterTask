import sqlite3
import sys
import traceback

from flask import Flask, render_template, g, redirect, request
from queries import *

app = Flask(__name__)
DATABASE = 'selection_committee.db'
last_request = None
last_exams = None
last_specialty = None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def index():
    return redirect('/results', code=302)


@app.route('/add_specialty', methods=['GET', 'POST'])
def add_specialty():
    data = {
        'success': False,
        'submitted': False
    }
    db = get_db()
    cur = db.cursor()
    data['exams'] = cur.execute(exam_id_name).fetchall()
    cur.close()

    if request.method == 'POST':
        data['submitted'] = True
        r = request.form
        name, num, level, form, exam1, exam2, exam3 = r['name'], r['num'], \
                                                      r['level'], r['form'], r['exam1'], r['exam2'], r['exam3']
        print(level)
        cur = db.cursor()
        try:
            cur.execute(specialty_insert, (name, num, form, level, exam1, exam2, exam3))
            data['success'] = True
            cur.close()
            db.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        cur.close()
    return render_template('main/add_specialty.html', data=data)


@app.route('/add_exam', methods=['GET', 'POST'])
def add_exam():
    data = {
        'success': False,
        'submitted': False
    }
    if request.method == 'POST':
        data['submitted'] = True
        db = get_db()
        cur = db.cursor()
        r = request.form
        name, min_ball = r['name'], r['min_ball']
        try:
            cur.execute(exam_insert, (name, min_ball))
            data['success'] = True
            cur.close()
            db.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        cur.close()
    return render_template('main/add_exam.html', data=data)


@app.route('/add_enrollee', methods=['GET', 'POST'])
def add_enrollee():
    data = {
        'success': False,
        'submitted': False
    }
    if request.method == 'POST':
        data['submitted'] = True
        db = get_db()
        cur = db.cursor()
        r = request.form
        fio, bonus = r['name'], r['bonus']
        try:
            cur.execute(enrollee_insert, (fio, bonus))
            data['success'] = True
            cur.close()
            db.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        cur.close()
    return render_template('main/add_enrollee.html', data=data)


@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    data = {
        'success': False,
        'submitted': False
    }
    db = get_db()
    cur = db.cursor()
    data['enrollee'] = cur.execute(enrollee_id_fio).fetchall()
    data['specialty'] = cur.execute(specialty_id_name).fetchall()
    cur.close()
    return render_template('main/add_request.html', data=data)


@app.route('/add_request_exams', methods=['GET', 'POST'])
def add_request_exams():
    data = {
        'success': False,
        'submitted': True,
        'exam_sub': True
    }
    r = request.form
    if 'success' not in r:
        specialty = r['specialty']
        db = get_db()
        cur = db.cursor()
        data['exams'] = cur.execute(specialty_exams, specialty).fetchall()
        global last_exams
        last_exams = data['exams']
        cur.close()
        global last_request
        last_request = (r['enrollee'], r['specialty'])
    if 'success' in r:
        data['submitted'] = True
        db = get_db()
        cur = db.cursor()
        enrollee, specialty, exam1, exam2, exam3 = \
            last_request[0], last_request[1], r['exam' + str(last_exams[0][0])], \
            r['exam' + str(last_exams[1][0])], r['exam' + str(last_exams[2][0])]
        try:
            cur.execute(request_insert, (enrollee, specialty, exam1, exam2, exam3))
            cur.close()
            db.commit()
            data['success'] = True
            data['exam_sub'] = False
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        cur.close()
    return render_template('main/add_request.html', data=data)


@app.route('/results', methods=['GET', 'POST'])
def results():
    data = {
        'success': False,
        'submitted': False
    }
    db = get_db()
    cur = db.cursor()
    data['specialty'] = cur.execute(specialty_id_name).fetchall()
    cur.close()
    if request.method == 'POST':
        data['submitted'] = True
        db = get_db()
        cur = db.cursor()
        r = request.form
        specialty = r['specialty']
        global last_specialty
        last_specialty = specialty
        try:
            data['exams'] = cur.execute(specialty_exams, specialty).fetchall()
            global last_exams
            last_exams = data['exams']
            data['res'] = cur.execute(result, specialty).fetchall()
            data['success'] = True
            cur.close()
            db.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        cur.close()
    return render_template('main/results.html', data=data)


@app.route('/statistics', methods=['GET', 'POST'])
def get_statistics():
    data = {
        'success': False,
        'submitted': False
    }
    db = get_db()
    cur = db.cursor()
    data['specialty'] = cur.execute(specialty_id_name).fetchall()
    cur.close()
    if request.method == 'POST':
        data['submitted'] = True
        db = get_db()
        cur = db.cursor()
        r = request.form
        specialty = r['specialty']
        try:
            data['exams'] = cur.execute(specialty_exams, specialty).fetchall()
            cnt = cur.execute(size, specialty).fetchall()[0][0]
            tmp = cur.execute(lst_of_balls, specialty).fetchall()
            data['last'] = tmp[min(len(tmp), cnt) - 1]
            data['res'] = cur.execute(lst_of_mean, specialty).fetchall()
            data['success'] = True
            cur.close()
            db.commit()
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        cur.close()
    return render_template('main/statistics.html', data=data)


@app.route('/edit', methods=['POST'])
def edit():
    r = request.form
    if 'edit' in r:
        db = get_db()
        cur = db.cursor()
        idx = cur.execute(get_id, (r['name'],)).fetchall()[0][0]
        exam1, exam2, exam3 = r['exam' + str(last_exams[0][0])], \
            r['exam' + str(last_exams[1][0])], r['exam' + str(last_exams[2][0])]
        cur.execute(edit_request, (exam1, exam2, exam3, idx, last_specialty))
        cur.close()
        db.commit()
    else:
        db = get_db()
        cur = db.cursor()
        idx = cur.execute(get_id, (r['name'],)).fetchall()[0][0]
        cur.execute(del_request, (idx,last_specialty))
        cur.close()
        db.commit()
    return redirect('/results')


if __name__ == '__main__':
    app.run()
