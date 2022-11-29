
CREATE TYPE students_table AS TABLE
(
	Class VARCHAR(20),
	FirstName VARCHAR(20),
	Grade INT
);



CREATE FUNCTION class_grades(@InputTable students_table READONLY)
RETURNS TABLE
AS 
RETURN
	SELECT
	s.Class,
	CAST(AVG(s.Grade) AS DECIMAL(6,1)) AS 'Median'
	FROM
	   (
		 SELECT
		 FirstName,
		 Class,
		 Grade,
		 ROW_NUMBER() OVER (
		 PARTITION BY Class
		 ORDER BY Grade ASC, ID ASC) AS RowAsc,
		 ROW_NUMBER() OVER (
		 PARTITION BY Class
		 ORDER BY Grade DESC, ID DESC) AS RowDesc
		 FROM students
	   ) AS s
	WHERE
	RowAsc IN (RowDesc, RowDesc - 1, RowDesc + 1)
	GROUP BY s.Class


CREATE TABLE students1 (
   Class varchar(50),
   FirstName varchar(50),
   Grade decimal(5,1)
)

INSERT INTO students1 
VALUES ('Math', 'Bob', 65),
		('Math', 'Joe', 72),
        ('Math', 'Sally', 95),
        ('Science', 'Bob', 65),
        ('Science', 'Joe', 81),
        ('Science', 'Sally', 81),
        ('Science', 'Mike', 72);

DECLARE @Tab AS students_table
INSERT @Tab 
SELECT * FROM students1

SELECT * FROM class_grades(@Tab)

