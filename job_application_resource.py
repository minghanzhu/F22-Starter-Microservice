import uuid

import pymysql
import os
import boto3

aws_region = "us-east-1"
# read the aws credentials from environment variables
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")


class JobApplicationResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        """
        Get a connection to the database
        :return: a connection to the database
        """
        # connect to the dynamodb database
        client = boto3.client("dynamodb", region_name=aws_region, aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)
        return client

    @classmethod
    def create_new_application(cls, application_data: dict):
        # create a random id for the application
        application_id = "app_" + str(uuid.uuid4())

        item = {
            "application_id": {
                "S": application_id
            },
            "applicant_id": {
                "S": application_data["applicant_id"]
            },
            "job_id": {
                "S": application_data["job_id"]
            }
        }
        # check if the applicant already applied for the job
        response = cls._get_connection().scan(
            TableName="application",
            FilterExpression="applicant_id = :applicant_id AND job_id = :job_id",
            ExpressionAttributeValues={
                ":applicant_id": {
                    "S": application_data["applicant_id"]
                },
                ":job_id": {
                    "S": application_data["job_id"]
                }
            }
        )
        if response["Count"] != 0:
            print("The applicant already applied for the job", application_data["applicant_id"],
                  application_data["job_id"])
            print("response: ", response)
            return "The applicant already applied for the job"

        # create a new item in the table
        response = cls._get_connection().put_item(
            TableName="application",
            Item=item,
        )
        # Append the new item to the response
        response["Item"] = item
        return response

    @classmethod
    def get_applications_by_applicant_id(cls, applicant_id):
        print("applicant_id: ", applicant_id)
        response = cls._get_connection().scan(
            TableName="application",
            FilterExpression="applicant_id = :applicant_id",
            ExpressionAttributeValues={
                ":applicant_id": {
                    "S": applicant_id
                }
            }
        )
        return response

    @classmethod
    def get_applications_by_job_id(cls, job_id):
        print("job_id: ", job_id)
        response = cls._get_connection().scan(
            TableName="application",
            FilterExpression="job_id = :job_id",
            ExpressionAttributeValues={
                ":job_id": {
                    "S": job_id
                }
            }
        )
        return response
