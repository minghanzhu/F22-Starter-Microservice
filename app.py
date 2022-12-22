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


# Get all job applications for a job
@app.route("/api/applications/<job_id>/posted", methods=["GET"])
def get_applications_by_job_id(job_id):
    print("job_id: ", job_id)
    result = JobApplicationResource.get_applications_by_job_id(job_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


# Create a new job
@app.route("/api/jobs", methods=["POST"])
def create_job():
    print("Create job")
    result = JobResource.create_new_job(request.json)
    if type(result) == dict:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
        # AWS SNS publish to topic
        JobResource.publish_job_to_sns(result)
    else:
        rsp = Response(result, status=409, content_type="text/plain")
    return rsp


# Get a job by job_id
@app.route("/api/jobs/<job_id>", methods=["GET"])
def get_job_by_id(job_id):
    print("job_id: ", job_id)
    result = JobResource.get_job_by_id(job_id)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
    return rsp


# Update a job
@app.route("/api/jobs/<job_id>", methods=["PUT"])
def update_job(job_id):
    print("Update job")
    result = JobResource.update_job(job_id, request.json)
    if type(result) == dict:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(result, status=404, content_type="text/plain")
    return rsp


# Delete a job
@app.route("/api/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    print("Delete job")
    result = JobResource.delete_job(job_id)
    if type(result) == dict:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response(result, status=404, content_type="text/plain")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
