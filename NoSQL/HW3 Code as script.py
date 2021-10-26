import boto3

s3 = boto3.resource('s3',
aws_access_key_id='',
aws_secret_access_key='' )

try:
    s3.create_bucket(Bucket='datacont-cs1660-2', CreateBucketConfiguration={
    'LocationConstraint': 'us-east-2'})
except Exception as e:
    print (e)

bucket = s3.Bucket("datacont-cs1660-2")

bucket.Acl().put(ACL='public-read')

body = open('exp1.csv', 'rb')

o = s3.Object('datacont-cs1660', 'test').put(Body=body)

s3.Object('datacont-cs1660', 'test').Acl().put(ACL='public-read')

dyndb = boto3.resource('dynamodb',
region_name='us-east-2',
aws_access_key_id='AKIARZJJXMDNDTT322RN',
aws_secret_access_key='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'
)

try:
    table = dyndb.create_table(
        TableName='DataTable2',
        KeySchema=[
            {
                'AttributeName': 'PartitionKey',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'RowKey',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PartitionKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'RowKey',
                'AttributeType': 'S'
            },
        ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
    )
except Exception as e:
    print (e)
#if there is an exception, the table may already exist.
    table = dyndb.Table("DataTable2")

table.meta.client.get_waiter('table_exists').wait(TableName='DataTable2')

print(table.item_count)

import csv

with open('experiments.csv', 'rt') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 1
    for item in csvf:
        if i == 1:
            i += 1
            continue
        print(item)
        body = open(item[4], 'rb')
        s3.Object('datacont-cs1660-2', item[4]).put(Body=body)
        md = s3.Object('datacont-cs1660-2', item[4]).Acl().put(ACL='public-read')
        url = "https://s3-us-west-2.amazonaws.com/datacont-cs1660-2/"+item[4]
        metadata_item = {
                         'PartitionKey': item[0],
                         'RowKey': item[1],
                         'Conductivity': item[2],
                         'Concentration': item[3],
                         'url':url
                        }
        try:
            table.put_item(Item=metadata_item)
        except:
            print("item may already be there or another failure")

response = table.get_item(
    Key={
        'PartitionKey': '1',
        'RowKey': '-1'
    }
)
item = response['Item']
print(item)
