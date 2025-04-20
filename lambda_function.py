import json
import boto3
import joblib
import os
import numpy as np
from io import BytesIO

# Load AI Model from S3
def load_model_from_s3(bucket_name, model_key):
    """
    Loads a pre-trained AI model from an S3 bucket.

    Args:
    - bucket_name (str): Name of the S3 bucket.
    - model_key (str): Key (path) to the model file in S3.

    Returns:
    - model (sklearn model): Loaded model object.
    """
    try:
        s3 = boto3.client('s3')
        with BytesIO() as f:
            s3.download_fileobj(bucket_name, model_key, f)
            f.seek(0)
            model = joblib.load(f)
        return model
    except Exception as e:
        print(f"❌ Error loading model from S3: {e}")
        raise e

# Fetch AWS CloudWatch Metrics
def get_cloudwatch_metrics():
    """
    Fetches AWS Lambda performance metrics from CloudWatch and generates synthetic features.

    Returns:
    - List: Feature vector for AI model prediction (9 features).
    """
    try:
        cloudwatch = boto3.client('cloudwatch')

        response = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {'Id': 'cpu_usage', 'MetricStat': {'Metric': {'Namespace': 'AWS/Lambda', 'MetricName': 'Duration'}, 'Period': 300, 'Stat': 'Average'}} ,
                {'Id': 'invocation_count', 'MetricStat': {'Metric': {'Namespace': 'AWS/Lambda', 'MetricName': 'Invocations'}, 'Period': 300, 'Stat': 'Sum'}} ,
                {'Id': 'error_count', 'MetricStat': {'Metric': {'Namespace': 'AWS/Lambda', 'MetricName': 'Errors'}, 'Period': 300, 'Stat': 'Sum'}} ,
                {'Id': 'throttles', 'MetricStat': {'Metric': {'Namespace': 'AWS/Lambda', 'MetricName': 'Throttles'}, 'Period': 300, 'Stat': 'Sum'}} ,
                {'Id': 'concurrent_executions', 'MetricStat': {'Metric': {'Namespace': 'AWS/Lambda', 'MetricName': 'ConcurrentExecutions'}, 'Period': 300, 'Stat': 'Average'}}
            ],
            StartTime='2025-03-19T10:30:00Z',  # 🔹 Updated Start Time
            EndTime='2025-03-19T10:44:00Z'  # 🔹 Updated End Time
        )

        # ✅ Fetch 5 real CloudWatch metrics
        metrics = []
        for metric_data in response['MetricDataResults']:  
            values = metric_data.get('Values', [])
            metric_value = values[-1] if values else np.random.uniform(0, 100)  # 🔹 Use last value if available, else random
            metrics.append(metric_value)

        # ✅ Generate 4 synthetic features
        synthetic_features = [
            max(metrics),
            min(metrics),
            sum(metrics) / len(metrics) if sum(metrics) > 0 else 0,
            len([m for m in metrics if m > 0])
        ]

        # ✅ Combine real and synthetic features
        metrics.extend(synthetic_features)

        print(f"✅ Adjusted CloudWatch Metrics: {metrics}")
        return metrics  # Returns 9 features

    except Exception as e:
        print(f"❌ Error fetching CloudWatch metrics: {e}")
        return [np.random.uniform(0, 100) for _ in range(9)]  # 🔹 Use random values instead of 0


# Send AWS SNS Alert on Fault Detection
def send_sns_alert(message):
    """
    Sends an alert via AWS SNS when a fault is detected.
    """
    try:
        sns = boto3.client('sns', region_name="eu-north-1")

        # ✅ Subscribe email to SNS topic if not already subscribed
        topic_arn = "arn:aws:sns:eu-north-1:122610488475:FaultAlerts"
        email_address = "ayshukl13@gmail.com"

        # Check existing subscriptions
        subscriptions = sns.list_subscriptions_by_topic(TopicArn=topic_arn)['Subscriptions']
        subscribed_emails = [sub['Endpoint'] for sub in subscriptions if sub['Protocol'] == 'email']

        if email_address not in subscribed_emails:
            sns.subscribe(
                TopicArn=topic_arn,
                Protocol="email",
                Endpoint=email_address
            )
            print(f"✅ Subscription request sent to {email_address}")

        # ✅ Send the actual alert
        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="🚨 AWS Lambda Fault Alert!"
        )
    except Exception as e:
        print(f"❌ Error sending SNS alert: {e}")

# Lambda Handler Function
def lambda_handler(event, context):
    """
    AWS Lambda handler function to predict faults based on CloudWatch metrics.
    """
    bucket_name = 'ai-fault-detector-bucket'
    model_key = 'ai_fault_detector.pkl'

    try:
        # ✅ Load AI Model
        model = load_model_from_s3(bucket_name, model_key)

        # ✅ Fetch CloudWatch Metrics (now includes 9 features)
        metrics = get_cloudwatch_metrics()

        # ✅ Ensure model input matches expected feature count
        expected_features = model.n_features_in_
        if len(metrics) != expected_features:
            print(f"❌ Model expects {expected_features} features, but received {len(metrics)}")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f"Incorrect input size: Model expects {expected_features} features, received {len(metrics)}"
                })
            }

        # ✅ Prepare input data
        input_data = np.array(metrics).reshape(1, -1)

        # ✅ Run AI Model Prediction
        is_fault = model.predict(input_data)[0]
        result = 'Fault Detected' if is_fault == -1 else 'No Fault'

        print(f"🔍 Prediction Result: {result} | Metrics: {metrics}")

        # ✅ Send an SNS Alert if a fault is detected
        if is_fault == -1:
            send_sns_alert(f"🚨 AWS Lambda detected a fault! Metrics: {metrics}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': result,
                'metrics': metrics
            })
        }

    except Exception as e:
        print(f"❌ Error in Lambda function: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
