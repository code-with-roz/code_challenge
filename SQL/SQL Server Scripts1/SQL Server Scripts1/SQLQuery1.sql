CREATE TABLE students (
   ID int identity(1,1),
   Class varchar(50),
   FirstName varchar(50),
   Grade decimal(5,1)
)


INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Math', 'Bob', 65)
INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Math', 'Joe', 72)
INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Math', 'Sally', 95)
INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Science', 'Bob', 65)
INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Science', 'Joe', 81)
INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Science', 'Sally', 81)
INSERT INTO students (Class, FirstName, Grade)
   VALUES ('Science', 'Mike', 72)

SELECT
x.Class,
CAST(AVG(x.Grade) AS DECIMAL(6,1)) AS 'Median'
FROM
   (
     SELECT
     Class,
     FirstName,
     Grade,
     ROW_NUMBER() OVER (
     PARTITION BY Class
     ORDER BY Grade ASC, ID ASC) AS RowAsc,
     ROW_NUMBER() OVER (
     PARTITION BY Class
     ORDER BY Grade DESC, ID DESC) AS RowDesc
     FROM @tmp
   ) AS x
WHERE
RowAsc IN (RowDesc, RowDesc - 1, RowDesc + 1)
GROUP BY x.Class
ORDER BY x.Class