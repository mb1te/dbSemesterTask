exam_id_name = 'SELECT id, name FROM Exam ORDER BY name'
enrollee_id_fio = 'SELECT id, fio FROM Enrollee ORDER BY fio'
specialty_id_name = 'SELECT id, name FROM Specialty ORDER BY name'
specialty_exams = 'SELECT Exam.id, Exam.name FROM Specialty JOIN Exam WHERE Specialty.id = ?' \
                  'AND Exam.id in (exam1_id, exam2_id, exam3_id)'

enrollee_insert = 'INSERT INTO Enrollee (fio, bonus_ball, date_of_birth) VALUES (?,?,?)'
specialty_insert = 'INSERT INTO Specialty (name, number_of_places, study_form, study_level, ' \
                   'exam1_id, exam2_id, exam3_id) VALUES (?,?,?,?,?,?,?)'
exam_insert = 'INSERT INTO Exam (name, min_ball) VALUES (?,?)'
request_insert = 'INSERT INTO Request (enrollee_id, specialty_id, exam1, exam2, exam3) VALUES (?,?,?,?,?)'

result = 'SELECT fio, exam1, exam2, exam3, bonus_ball, exam1 + exam2 + exam3 + bonus_ball as res ' \
         'FROM Request JOIN Enrollee ON Request.enrollee_id = Enrollee.id ' \
         'WHERE Request.specialty_id = ? ORDER BY res DESC;'

lst_of_balls = 'SELECT exam1 + exam2 + exam3 + bonus_ball as res ' \
             'FROM Request JOIN Enrollee ON Request.enrollee_id = Enrollee.id ' \
             'WHERE Request.specialty_id = ? ORDER BY res DESC;'

lst_of_mean = 'SELECT AVG(exam1), AVG(exam2), AVG(exam3), AVG(bonus_ball), ' \
              'AVG(exam1 + exam2 + exam3 + bonus_ball) FROM Request ' \
              'JOIN Enrollee ON Request.enrollee_id = Enrollee.id ' \
              'WHERE Request.specialty_id = ?'

size = 'SELECT number_of_places FROM Specialty WHERE id = ?'

del_request = 'DELETE FROM Request WHERE enrollee_id = ? AND specialty_id = ?'

edit_request = 'UPDATE Request SET exam1 = ?, exam2 = ?, exam3 = ? WHERE enrollee_id = ? AND specialty_id = ?'

get_id = 'SELECT id FROM Enrollee WHERE fio = ?'
