import json, urllib, boto3, csv
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
HMOsTable = dynamodb.Table('HMOs');

def lambda_handler(event, context):
    # Show the incoming event in the debug log
    # print("Event received by Lambda function: " + json.dumps(event, indent=2))
    
    requestBody = json.loads(event['body'])
    print(requestBody)
    
    
    # extract details from event and put in Db
    try:
        name = requestBody["companyName"]
        subscription = requestBody["subscription"]
        website = requestBody["website"]
        contact = requestBody["contact"]
        email = requestBody["email"]
        
        HMOsTable.put_item(
            Item={
                "name":name,
                "subscription":subscription,
                "website": website,
                "contact":contact,
                "email":email
            })
        
    except Exception as e:
        print(e)
        print("Unable to insert data into DynamoDB table".format(e))
        return {
            'statusCode': 500,
            'body': json.dumps('internal server error')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('registration successful')
    }
