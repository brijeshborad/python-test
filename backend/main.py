from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/send-email", methods=['POST', 'OPTIONS'])
@cross_origin(origin='*')
def send_email():
    request_data = request.get_json()
    email_data = send_email_using_aws(request_data.get('email'))
    return jsonify({'success': True if email_data is not None else False})


def send_email_using_aws(email=None):
    response_data = None
    sender = "Sender Name <brijeshborad29@gmail.com>"
    recipient = "brijeshrockss@gmail.com"

    # if email is not None:
    #     recipient = email

    aws_region = "us-east-2"
    subject = "Test Email"
    body_text = ("Test email body.")

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>Test email</h1>
      <p>Test email with python on lambda</p>
    </body>
    </html>"""

    charset = "UTF-8"
    aws_s3_creds = {
        "aws_access_key_id": "AKIAXGYYVA2O4QXILQLN",  # os.getenv("AWS_ACCESS_KEY")
        "aws_secret_access_key": "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"  # os.getenv("AWS_SECRET_KEY")
    }

    client = boto3.client('ses', region_name=aws_region, **aws_s3_creds)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender
        )
    except ClientError as e:
        # response_data = e.response['Error']['Message']
        response_data = None
    else:
        response_data = response['MessageId']

    return response_data


if __name__ == "__main__":
    app.run(debug=True)
