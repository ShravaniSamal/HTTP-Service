from flask import Flask, jsonify, request
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)

# AWS credentials and bucket details
BUCKET_NAME = "mybucket1320"
AWS_REGION = "ap-south-1"
AWS_ACCESS_KEY = "*************"
AWS_SECRET_KEY = "****************************"

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    region_name="ap-south-1",
    aws_access_key_id="*************",
    aws_secret_access_key="****************************",
)

@app.route('/list-bucket-content', defaults={'path': ''}, methods=['GET'])
@app.route('/list-bucket-content/<path:path>', methods=['GET'])
def list_bucket_content(path):
    try:
        prefix = path + '/' if path and not path.endswith('/') else path
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter='/')

        content = []
        if 'CommonPrefixes' in response:
            content.extend([prefix['Prefix'].rstrip('/').split('/')[-1] for prefix in response['CommonPrefixes']])
        if 'Contents' in response:
            content.extend([obj['Key'].split('/')[-1] for obj in response['Contents'] if obj['Key'] != prefix])

        return jsonify({"content": content}), 200

    except ClientError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
