import sys
import os
from flask import Flask, Response, request
from datetime import datetime
import json
from flask_cors import CORS
from job_application_resource import JobApplicationResource
from job_resource import JobResource

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.route('/')
def index():
    return "Hello World"


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


# Get all job applications for an applicant
@app.route("/api/applications/<applicant_id>/applied", methods=["GET"])
def get_applications_by_applicant_id(applicant_id):
    print("applicant_id: ", applicant_id)
    result = JobApplicationResource.get_applications_by_applicant_id(applicant_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


# Create a new job application
@app.route("/api/applications", methods=["POST"])
def create_application():
    print("Create application")
    result = JobApplicationResource.create_new_application(request.json)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        # if the applicant already applied for the job, return 409
        rsp = Response("CONFLICT", status=409, content_type="text/plain")
    return rsp


# Create a new job
@app.route("/api/jobs", methods=["POST"])
def create_job():
    print("Create job")
    result = JobResource.create_new_job(request.json)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("CONFLICT", status=409, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
