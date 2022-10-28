import pymysql

import os


class CourseResource:
    """
    Sections table:
    create table sections
    (
        call_no int      not null
            primary key,
        title   char(24) null
    );

    Projects table:
    create table projects
    (
    `project id`   int  not null
        primary key,
    `project name` char null
    );

    Enrollments table:
    create table enrollments
    (
    call_no    int      not null,
    UNI        char(16) not null,
    project_id int      not null,
    primary key (project_id, UNI)
    );
    """

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user="root",
            password="dbuserdbuser",
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_all_sections():
        sql = "SELECT * FROM f22_databases.sections";
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_section_by_call_no(call_no):
        sql = "SELECT * FROM f22_databases.sections WHERE call_no=%s";
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (call_no,))
        result = cur.fetchone()

        return result

    @staticmethod
    def get_enrollments_by_call_no(call_no):
        sql = "SELECT * FROM f22_databases.enrollments WHERE call_no=%s";
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (call_no,))
        result = cur.fetchall()

        return result
