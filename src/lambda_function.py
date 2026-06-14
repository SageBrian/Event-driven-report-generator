import os
import boto3
import csv
import json

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Parse incoming S3 bucket and object key info
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    dest_bucket = os.environ['DEST_BUCKET']
    
    print(f"Processing file {object_key} from bucket {source_bucket}")
    
    # 2. Download the CSV file into memory
    csv_file_obj = s3_client.get_object(Bucket=source_bucket, Key=object_key)
    csv_content = csv_file_obj['Body'].read().decode('utf-8').splitlines()
    
    # 3. Simple processing step (parsing rows)
    reader = csv.DictReader(csv_content)
    total_records = 0
    parsed_data = []
    
    for row in reader:
        total_records += 1
        parsed_data.append(row)
        
    # 4. Generate a clean summary report text file (Simulating a report output)
    report_key = f"reports/summary-{object_key.replace('.csv', '')}.txt"
    report_content = f"""
    =============================================
    AUTOMATED CLOUD PROCESSING REPORT
    =============================================
    Original File: {object_key}
    Total Records Processed: {total_records}
    Status: SUCCESS
    
    Raw Payload Summary:
    {json.dumps(parsed_data, indent=2)}
    =============================================
    """
    
    # 5. Save the generated report into our Destination bucket
    s3_client.put_object(
        Bucket=dest_bucket,
        Key=report_key,
        Body=report_content,
        ContentType='text/plain'
    )
    
    print(f"Successfully generated and saved report to {dest_bucket}/{report_key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete!')
    }