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
                    localFilename = '/tmp/claim.txt'
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
                            
                            # compute claim status for each categories
                            claim_status = None
                            # Motorcycle
                            if(row["category"]=="motorcycle"):
                                if(int(row['compensationAmount'])>5000):
                                    claim_status = "review"
                                else:
                                    claim_status = "pay"
                            # car
                            if(row["category"]=="car"):
                                if(int(row['compensationAmount'])>10000):
                                    claim_status = "review"
                                else:
                                    claim_status = "pay"
                            # van
                            if(row["category"]=="van"):
                                if(int(row['compensationAmount'])>15000):
                                    claim_status = "review"
                                else:
                                    claim_status = "pay"    
                            
                            claimTable.put_item(
                                Item={
                                    'id':str(uuid.uuid4()),
                                    'companyName':row['company'],
                                    'category':row["category"],
                                    'model':row['model'],
                                    'brand':row['brand'],
                                    'compensationAmount':row['compensationAmount'],
                                    'claim_status': claim_status
                                }
                                )
                            
    except Exception as exception:
        print(exception)
    