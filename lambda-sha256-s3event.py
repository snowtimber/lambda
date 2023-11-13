import json
import urllib.parse
import boto3
import hashlib

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(bucket)
    print(key)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        # return response['ContentType']
        
        # Fetch the object
        # obj = s3.get_object(Bucket=bucket, Key=key)
        
        # Calculate the SHA256 checksum
        sha256 = hashlib.sha256()
        for chunk in iter(lambda: response['Body'].read(4096), b""):
            sha256.update(chunk)
        
        checksum = sha256.hexdigest()
        print(f"SHA256 Checksum for {bucket}/{key}: {checksum}")
    
        # Return the checksum (or store it somewhere like DynamoDB, another S3 object, etc.)
        return checksum
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
