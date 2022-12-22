import os
import boto3
import botocore

aws_region = "us-east-1"
# read the aws credentials from environment variables
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")


class JobResource:

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
    def create_new_job(cls, job_data: dict):
        item = {
            "job_id": {
                "S": job_data["job_id"]
            },
            "company_name": {
                "S": job_data["company_name"],
            },
            "role": {
                "S": job_data["role"]
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
