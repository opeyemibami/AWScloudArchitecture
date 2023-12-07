#claim statistics lambda function 
import json, boto3
from datetime import datetime
currentDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    # Show the incoming event in the debug log
    # print("Event received by Lambda function: " + json.dumps(event, indent=2))
    pay_count = 0
    review_count = 0
    review_ids = []
    autoVetstats = None
    companyName = None
    for record in event['Records']:
        newImage = record['dynamodb'].get('NewImage', None)
        if(newImage):
            # print record in debug log
            print("#######################",newImage)
            companyName = newImage['companyName']['S']
            if(newImage['claim_status']['S']=='pay'):
                pay_count+=1
            else:
                review_count+=1
                review_ids.append(newImage['id']['S'])
    if(len(review_ids)>0):
        autoVetstats = round((pay_count/(review_count+pay_count))*100,2)
    totalClaims = pay_count+review_count
    if(totalClaims>0):    
        # print("review_count: ",review_count,"pay_count: ",pay_count,"review_ids: ",review_ids,"autoVetstats: ",autoVetstats) 
        R = "\nReview Counts = " + str(review_count)
        P = "\nPay Counts = " + str(pay_count)
        RiDs = "\nReview IDs = " + str(review_ids)
        AutoVetPercentage = "\nAutoVetPercentage = " + str(autoVetstats) + "%"
        greetings = "Company Name= "+companyName + "\nProcessDate: "+ currentDate 
        message = greetings + "\nBatch ID = 12345" + R + P + RiDs +AutoVetPercentage
        print(message)
        
        # Connect to SNS
        sns = boto3.client('sns')
        alertTopic = 'ClaimsStatistics'
        snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics'] if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0]
        
        # Send message to SNS
        sns.publish(
            TopicArn=snsTopicArn,
            Message=message,
            Subject='Claims Statistics Report',
            MessageStructure='raw'
            )
        return 'Statistics processing successful'
    return 'no new claim to process'