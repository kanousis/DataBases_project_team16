BEGIN TRANSACTION;

DROP TABLE IF EXISTS "STUDENT";
CREATE TABLE IF NOT EXISTS "STUDENT" (
	"student_id" integer NOT NULL,
	"current_semester" integer NOT NULL,
	"department" varchar NOT NULL,
	"credits" decimal,
	PRIMARY KEY ("student_id"),
	FOREIGN KEY ("student_id") REFERENCES "MEMBER" ("member_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "MEMBER";
CREATE TABLE IF NOT EXISTS "MEMBER" (
	"member_id" integer NOT NULL,
	"first_name" varchar NOT NULL,
	"last_name" varchar NOT NULL,
	"street" varchar,
	"number" integer,
	"PC" varchar,
	"email" varchar,
	"telephone" integer,
	"password" varchar NOT NULL,
	PRIMARY KEY ("member_id")
);

DROP TABLE IF EXISTS "PROFESSOR";
CREATE TABLE IF NOT EXISTS "PROFESSOR" (
	"professor_id" integer NOT NULL,
	PRIMARY KEY ("professor_id"),
	FOREIGN KEY ("professor_id") REFERENCES "MEMBER" ("member_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "COURSE";
CREATE TABLE IF NOT EXISTS "COURSE" (
	"course_id" varchar NOT NULL,
	"title" varchar NOT NULL,
	"semester" integer NOT NULL,
	PRIMARY KEY ("course_id", "semester")
);

DROP TABLE IF EXISTS "COURSE_TEACHING";
CREATE TABLE IF NOT EXISTS "COURSE_TEACHING" (
	"course_id" varchar NOT NULL,
	"semester" integer NOT NULL,
	"academic_year" varchar NOT NULL,
	"professor_id" integer,
	PRIMARY KEY ("course_id", "semester", "academic_year"),
	FOREIGN KEY ("course_id") REFERENCES "COURSE" ("course_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("semester") REFERENCES "COURSE" ("semester")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,		
	FOREIGN KEY ("professor_id") REFERENCES "PROFESSOR" ("professor_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "BOOK";
CREATE TABLE IF NOT EXISTS "BOOK" (
	"ISBN" varchar NOT NULL,
	"title" varchar NOT NULL,
	"author" varchar,
	"pages_number" integer,
	"publisher" varchar,
	"contents" blob,
	"cover" blob,
	"credits" decimal NOT NULL,
	"average_grade" decimal DEFAULT NULL,
	PRIMARY KEY ("ISBN")
);

DROP TABLE IF EXISTS "APPLICATION";
CREATE TABLE IF NOT EXISTS "APPLICATION" (
	"application_id" integer NOT NULL,
	"date" datetime NOT NULL,
	"semester" integer NOT NULL,
	"student_id" integer NOT NULL,
	PRIMARY KEY ("application_id"),
	FOREIGN KEY ("student_id") REFERENCES "STUDENT" ("student_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "PICKUP_POINT";
CREATE TABLE IF NOT EXISTS "PICKUP_POINT" (
	"pickup_point_id" integer NOT NULL,
	"name" varchar NOT NULL,
	"street" varchar,
	"number" integer,
	"PC" varchar,
	"telephone" integer,
	"email" varchar,
	PRIMARY KEY ("pickup_point_id")
);

DROP TABLE IF EXISTS "PICKUP";
CREATE TABLE IF NOT EXISTS "PICKUP" (
	"pickup_point_id" integer NOT NULL,
	"pickup_id" integer NOT NULL,
	"date" datetime NOT NULL,
	"application_id" integer NOT NULL,
	"student_id" integer NOT NULL,
	PRIMARY KEY ("pickup_id"),
	FOREIGN KEY ("pickup_point_id") REFERENCES "PICKUP_POINT
" ("pickup_point_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("application_id") REFERENCES "APPLICATION" ("application_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("student_id") REFERENCES "STUDENT" ("student_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "RETURN";
CREATE TABLE IF NOT EXISTS "RETURN" (
	"return_id" integer NOT NULL,
	"date" datetime NOT NULL,
	"student_id" integer NOT NULL,
	"pickup_point_id" integer NOT NULL,
	PRIMARY KEY ("return_id"),
	FOREIGN KEY ("student_id") REFERENCES "STUDENT" ("student_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("pickup_point_id") REFERENCES "PICKUP_POINT
" ("pickup_point_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Participates";
CREATE TABLE IF NOT EXISTS "Participates" (
	"course_id" varchar NOT NULL,
	"academic_year" datetime NOT NULL , 
	"ISBN" varchar NOT NULL,
	"book_suggestion" boolean,
	PRIMARY KEY ("course_id", "academic_year", "ISBN"),
	FOREIGN KEY ("course_id") REFERENCES "COURSE_TEACHING" ("course_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("academic_year") REFERENCES "COURSE_TEACHING" ("academic_year")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("ISBN") REFERENCES "BOOK" ("ISBN")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Consists_Of";
CREATE TABLE IF NOT EXISTS "Consists_Of" (
	"application_id" integer NOT NULL,
	"ISBN" varchar NOT NULL, 
	PRIMARY KEY ("application_id", "ISBN"),
	FOREIGN KEY ("application_id") REFERENCES "APPLICATION" ("application_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("ISBN") REFERENCES "BOOK" ("ISBN")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "It_Has";
CREATE TABLE IF NOT EXISTS "It_Has" (
	"pickup_point_id" integer NOT NULL,
	"ISBN" varchar NOT NULL, 
	PRIMARY KEY ("pickup_point_id", "ISBN"),
	FOREIGN KEY ("pickup_point_id") REFERENCES "PICKUP_POINT" ("pickup_point_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("ISBN") REFERENCES "BOOK" ("ISBN")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Contains(PICKUP-BOOK)";
CREATE TABLE IF NOT EXISTS "Contains(PICKUP-BOOK)" (
	"pickup_id" integer NOT NULL,
	"ISBN" varchar NOT NULL,
	PRIMARY KEY ("pickup_id", "ISBN"),
	FOREIGN KEY ("pickup_id") REFERENCES "PICKUP" ("pickup_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("ISBN") REFERENCES "BOOK" ("ISBN")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Contains(RETURN-BOOK)";
CREATE TABLE IF NOT EXISTS "Contains(RETURN-BOOK)" (
	"return_id" integer NOT NULL,
	"ISBN" varchar NOT NULL,
	PRIMARY KEY ("return_id", "ISBN"),
	FOREIGN KEY ("return_id") REFERENCES "RETURN" ("return_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("ISBN") REFERENCES "BOOK" ("ISBN")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Checks";
CREATE TABLE IF NOT EXISTS "Checks" (
	"pickup_id" integer NOT NULL,
	"return_id" integer NOT NULL,
	PRIMARY KEY ("pickup_id", "return_id"),
	FOREIGN KEY ("pickup_id") REFERENCES "PICKUP" ("pickup_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
	FOREIGN KEY ("return_id") REFERENCES "RETURN" ("return_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

DROP TABLE IF EXISTS "Rates";
CREATE TABLE IF NOT EXISTS "Rates" (
	"ISBN" varchar NOT NULL,
	"student_id" integer NOT NULL,
	"comment" text,
	"grade" decimal,
	PRIMARY KEY ("ISBN", "student_id"),
	FOREIGN KEY ("ISBN") REFERENCES "BOOK" ("ISBN")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("student_id") REFERENCES "STUDENT" ("student_id")
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);