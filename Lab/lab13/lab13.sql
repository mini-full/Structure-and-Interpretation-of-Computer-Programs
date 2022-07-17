.read data.sql

-- CREATE TABLE students(
--   time,
--   number,
--   color,
--   seven,
--   song,
--   date,
--   pet,
--   instructor,
--   smallest
-- );
-- CREATE TABLE numbers(
--   time,
--   "0",
--   "1",
--   "2",
--   "3",
--   "4",
--   "5",
--   "6",
--   "7",
--   "8",
--   "9",
--   "10",
--   "2021",
--   "2022",
--   "9000",
--   "9001"
-- );

CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = 'blue' AND pet = 'dog';

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = 'blue' AND pet = 'dog';


CREATE TABLE smallest_int_having AS
  SELECT time, smallest FROM students GROUP BY smallest HAVING count(smallest) = 1;


CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color FROM students AS a, students AS b WHERE a.pet = b.pet AND a.song = b.song AND a.time < b.time;


CREATE TABLE sevens AS
  SELECT seven FROM students, numbers WHERE students.time = numbers.time AND students.number = 7 AND numbers."7" ="True";


CREATE TABLE avg_difference AS
  SELECT round(avg(abs(number - smallest))) FROM students;

