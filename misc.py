# Load-Inventory Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file is downloaded and each line is inserted into a DynamoDB table.
import json, urllib, boto3, csv
# Connect to S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
# Connect to the DynamoDB tables
inventoryTable = dynamodb.Table('Inventory');
# This handler is run every time the Lambda function is triggered
def lambda_handler(event, context):
  # Show the incoming event in the debug log
  print("Event received by Lambda function: " + json.dumps(event, indent=2))
  # Get the bucket and object key from the Event
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
  localFilename = '/tmp/inventory.txt'
  # Download the file from S3 to the local filesystem
  try:
    s3.meta.client.download_file(bucket, key, localFilename)
  except Exception as e:
    print(e)
    print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
    raise e
  # Read the Inventory CSV file
  with open(localFilename) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    # Read each row in the file
    rowCount = 0
    for row in reader:
      rowCount += 1
      # Show the row in the debug log
      print(row['store'], row['item'], row['count'])
      try:
        # Insert Store, Item and Count into the Inventory table
        inventoryTable.put_item(
          Item={
            'Store':  row['store'],
            'Item':   row['item'],
            'Count':  int(row['count'])})
      except Exception as e:
         print(e)
         print("Unable to insert data into DynamoDB table".format(e))
    # Finished!
    return "%d counts inserted" % rowCount




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



{
    "companyName":"YelloLife",
    "claims" : [
        {"category":"car",
        "model":"2010",
        "brand":"BMW",
        "compensationAmount":10000},
        {
        "category":"motorcycle",
        "model":"2015",
        "brand":"Ducati",
        "compensationAmount":5000
        }
    ]
}



import json, urllib, boto3, csv, uuid
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
claimTable = dynamodb.Table('claims')

def lambda_handler(event, context):
    print(event)
    try:
        for i in event['Records']:
            s3_event = json.loads(i['body'])
            if 'Event' in s3_event and s3_event['Event'] == 's3:TestEvent':
                print("Test Event")
            else:
                for j in s3_event['Records']:
                    # print("Bucket Name : {} ".format(j['s3']['bucket']['name']))
                    # print("Object Name : {} ".format(j['s3']['object']['key']))
                    bucket = j['s3']['bucket']['name']
                    key = urllib.parse.unquote_plus(j['s3']['object']['key'])
                    localFilename = '/tmp/inventory.txt'
                    try:
                        s3.meta.client.download_file(bucket, key, localFilename)
                        print("file successfuly downloaded")
                    except Exception as e:
                        print(e)
                        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
                        raise e
                        
                    with open(localFilename) as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=',')
                        # Read each row in the file
                        rowCount = 0
                        for row in reader:
                            rowCount += 1
                            print(row["category"],row["model"],row['brand'],row['compensationAmount'])
                            
                            claimTable.put_item(
                                Item={
                                    'id':str(uuid.uuid4()),
                                    'category':row["category"],
                                    'model':row['model'],
                                    'brand':row['brand'],
                                    'compensationAmount':row['compensationAmount']
                                }
                                )
                            
    except Exception as exception:
        print(exception)
    


# Stock Check Lambda function
#
# This function is triggered when values are inserted into the Inventory DynamoDB table.
# Inventory counts are checked and if an item is out of stock, a notification is sent to an SNS Topic.
import json, boto3
# This handler is run every time the Lambda function is triggered
def lambda_handler(event, context):
  # Show the incoming event in the debug log
  print("Event received by Lambda function: " + json.dumps(event, indent=2))
  # For each inventory item added, check if the count is zero
  for record in event['Records']:
    newImage = record['dynamodb'].get('NewImage', None)
    if newImage:      
      count = int(record['dynamodb']['NewImage']['Count']['N'])  
      if count == 0:
        store = record['dynamodb']['NewImage']['Store']['S']
        item  = record['dynamodb']['NewImage']['Item']['S']  
        # Construct message to be sent
        message = store + ' is out of stock of ' + item
        print(message)  
        # Connect to SNS
        sns = boto3.client('sns')
        alertTopic = 'NoStock'
        snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics']
                        if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0]  
        # Send message to SNS
        sns.publish(
          TopicArn=snsTopicArn,
          Message=message,
          Subject='Inventory Alert!',
          MessageStructure='raw'
        )
  # Finished!
  return 'Successfully processed {} records.'.format(len(event['Records']))