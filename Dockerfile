# Use the AWS Lambda Python runtime
FROM public.ecr.aws/lambda/python:3.9

# Set working directory
WORKDIR /var/task

# Copy function code and dependencies
COPY lambda_function.py . 
COPY requirements.txt .

# Install dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Set the correct Lambda handler
CMD ["lambda_function.lambda_handler"]
