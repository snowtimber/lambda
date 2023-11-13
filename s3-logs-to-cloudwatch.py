import boto3
import json

s3_client = boto3.client('s3')
logs_client = boto3.client('logs')

def lambda_handler(event, context):
    # Get bucket name and key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Get the log file content from S3
    log_file = s3_client.get_object(Bucket=bucket_name, Key=key)
    log_content = log_file['Body'].read()

    # Define the CloudWatch Logs group and stream names
    log_group_name = 'YourLogGroupName'
    log_stream_name = 'YourLogStreamName'

    # Check if the log stream exists, if not, create it
    try:
        logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        # The log stream already exists, no action needed
        pass

    # Put log events to the CloudWatch log stream
    logs_client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
                'timestamp': int(context.get_remaining_time_in_millis()),
                'message': log_content.decode('utf-8')
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Log transferred to CloudWatch')
    }
