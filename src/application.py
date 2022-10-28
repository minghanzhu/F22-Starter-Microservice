from flask import Flask, Response, request
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from course_resource import CourseResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


# Get a student by id
@app.route("/api/students/<uni>", methods=["GET"])
def get_student_by_uni(uni):
    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


# Get all students
@app.route("/api/students", methods=["GET"])
def get_all_students():
    result = ColumbiaStudentResource.get_all()
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


# Get all sections
@app.route("/api/sections", methods=["GET"])
def get_all_sections():
    result = CourseResource.get_all_sections()
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


# Get a section by call number
@app.route("/api/sections/<call_no>", methods=["GET"])
def get_section_by_call_no(call_no):
    result = CourseResource.get_section_by_call_no(call_no)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


# Get all enrollments for a section
@app.route("/api/sections/<call_no>/enrollments", methods=["GET"])
def get_projects_by_call_no(call_no):
    result = CourseResource.get_enrollments_by_call_no(call_no)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
