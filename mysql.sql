
--SELECT Course.course_name
-- SELECT *
-- FROM StudentCourse INNER JOIN Course
-- ON StudentCourse.course_code = Course.course_code
-- WHERE StudentCourse.student_id = 'CD00100200314';


--SELECT Address.street,Address.city
-- SELECT *
-- FROM Student INNER JOIN Address
-- ON Student.address_id = Address.address_id
-- WHERE Student.first_name = 'Kamala' AND Student.last_name = 'Khan';


-- SELECT Review.completeness,Review.efficiency,Review.style,Review.documentation,Review.review_text
-- SELECT *
-- FROM Review 
-- WHERE Review.student_id = 'CD00100200314';


-- SELECT Course.course_name
-- SELECT *
-- FROM Course
-- WHERE Course.teacher_id = 'MZ004';


-- SELECT StudentCourse.student_id,Student.first_name,Student.last_name,Student.email,Course.course_name
-- SELECT *
-- FROM Student INNER JOIN StudentCourse INNER JOIN Course
-- ON Student.student_id = StudentCourse.student_id
-- AND StudentCourse.course_code = Course.course_code
-- WHERE is_complete = 0;


-- SELECT StudentCourse.student_id,Student.first_name,Student.last_name,Student.email,Course.course_name,StudentCourse.mark
-- SELECT *
-- FROM Student INNER JOIN StudentCourse INNER JOIN Course
-- ON Student.student_id = StudentCourse.student_id
-- AND StudentCourse.course_code = Course.course_code
-- WHERE is_complete = 1 AND mark <= 30;
