import boto3

def generate_table():
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8000',
                         region_name='example',                 # note that if you create a table using different region name and aws key
                         aws_access_key_id='example',           # you won't see this table on the admin app
                         aws_secret_access_key='example')

    ddb.create_table(
        TableName='UserDetails',                # create table Recipes
        AttributeDefinitions=[
            {
                'AttributeName': 'uid',     # In this case, I only specified uid as partition key (there is no sort key)
                'AttributeType': 'S'        # with type string
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'uid',     # attribute uid serves as partition key
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={             # specying read and write capacity units
            'ReadCapacityUnits': 100,        # these two values really depend on the app's traffic
            'WriteCapacityUnits': 100
        }
    )
    print('Successfully created table UserDetails')

generate_table()