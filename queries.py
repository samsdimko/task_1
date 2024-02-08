ROOMS_WITH_COUNT_STUDENTS_QUERY = ('SELECT rooms.name, count(*) as count_students FROM student_classes.rooms '
                                   'inner join student_classes.students on rooms.id = students.roomId '
                                   'group by rooms.name '
                                   'order by rooms.name')

ROOMS_WITH_MIN_AVERAGE_AGE_QUERY = (
    'SELECT rooms.name, cast(avg(TIMESTAMPDIFF(YEAR, birthday, CURDATE())) as float) as average_age '
    'FROM student_classes.rooms inner join student_classes.students on rooms.id = students.roomId '
    'group by rooms.name '
    'order by avg(TIMESTAMPDIFF(YEAR, birthday, CURDATE())) '
    'LIMIT 5')

ROOMS_WITH_MAXIMUM_DIFFERENCE_IN_AGE_QUERY = ('SELECT rooms.name, '
                                              'cast(MAX(TIMESTAMPDIFF(YEAR, birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, birthday, CURDATE())) '
                                              'as float) as age_difference '
                                              'FROM student_classes.rooms inner join student_classes.students on rooms.id = students.roomId '
                                              'group by rooms.name '
                                              'order by MAX(TIMESTAMPDIFF(YEAR, birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, birthday, CURDATE())) '
                                              'desc '
                                              'LIMIT 5')

ROOMS_WITH_BOTH_SEXES_QUERY = ('SELECT distinct rooms.name '
                               'FROM student_classes.rooms '
                               'where id in (select roomId from students where sex = \'M\') '
                               'and id in (select roomId from students where sex = \'F\')')
