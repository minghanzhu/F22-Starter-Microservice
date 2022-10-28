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
        """
        Get a connection to the database
        :return: a connection to the database
        """
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
        """
        Returns a list of all sections in the database.
        :return: list of all sections
        """
        sql = "SELECT * FROM f22_databases.sections";
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_section_by_call_no(call_no):
        """
        Returns a section with the given call number.
        :param call_no: call number of the section
        :return: section
        """
        sql = "SELECT * FROM f22_databases.sections WHERE call_no=%s";
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (call_no,))
        result = cur.fetchone()

        return result

    @staticmethod
    def get_enrollments_by_call_no(call_no):
        """
        Returns a list of enrollments for the given call number.
        :param call_no: call_no of the section
        :return: a list of enrollments
        """
        sql = "SELECT * FROM f22_databases.enrollments WHERE call_no=%s";
        conn = CourseResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (call_no,))
        result = cur.fetchall()

        return result
