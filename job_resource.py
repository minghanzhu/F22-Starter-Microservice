import json
import os
import boto3
import botocore
from botocore.exceptions import ClientError

aws_region = "us-east-1"
# read the aws credentials from environment variables
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")


class JobResource:

    def __int__(self):
        pass

    @classmethod
    def create_new_job(cls, job_data: dict):
        item = {
            "job_id": {
                "S": job_data["job_id"]
            },
            "company_name": {
                "S": job_data["company_name"],
            },
            "title": {
                "S": job_data["title"]
            },
            "job_description": {
                "S": job_data["job_description"]
            },
        }

        # create a new item in the table
        try:
            response = cls._get_connection().put_item(
                TableName="job",
                Item=item,
                # check if the job already exists
                ConditionExpression="attribute_not_exists(job_id)"
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return "Job already exists"
            else:
                return "Unknown error"
        # Append the new item to the response
        response["Item"] = item
        return response

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
    def get_job_by_id(cls, job_id):
        response = cls._get_connection().get_item(
            TableName="job",
            Key={
                "job_id": {
                    "S": job_id
                }
            }
        )
        return response

    @classmethod
    def update_job(cls, job_id: str, job_data: dict):
        # update the item in the table
        try:
            response = cls._get_connection().update_item(
                TableName="job",
                Key={
                    "job_id": {
                        "S": job_id
                    }
                },
                # check if the job already exists
                ConditionExpression="attribute_exists(job_id)",
                UpdateExpression="set company_name = :company_name, title = :title, job_description = "
                                 ":job_description",
                ExpressionAttributeValues={
                    ":company_name": {
                        "S": job_data["company_name"]
                    },
                    ":title": {
                        "S": job_data["title"]
                    },
                    ":job_description": {
                        "S": job_data["job_description"]
                    }
                },
                ReturnValues="UPDATED_NEW"
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return "Job does not exist"
            else:
                return "Unknown error"
        return response

    @classmethod
    def delete_job(cls, job_id: str):
        try:
            response = cls._get_connection().delete_item(
                TableName="job",
                Key={
                    "job_id": {
                        "S": job_id
                    }
                },
                # check if the job exists
                ConditionExpression="attribute_exists(job_id)"
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                return "Job does not exist"
            else:
                return "Unknown error"
        return response

    @classmethod
    def publish_job_to_sns(cls, job_data: dict):
        # publish the job to SNS
        sns_client = boto3.client("sns", region_name=aws_region, aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
        job_data = job_data["Item"]
        msg = f"New job posted: {job_data['title']['S']} at {job_data['company_name']['S']}"

        # publish the job to SNS
        response = sns_client.publish(
            TopicArn="arn:aws:sns:us-east-1:214792602728:new-job-alert-topic",
            Message=json.dumps(msg),
            Subject="New job posted"
        )
        return response
