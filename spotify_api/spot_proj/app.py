import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define table parameters
table_name = 'spotify_user_table'
key_schema = [
    {
        'AttributeName': 'UserID',
        'KeyType': 'HASH'  # Hash key
    }
]
attribute_definitions = [
    {
        'AttributeName': 'UserID',
        'AttributeType': 'S'  # String type
    }
]
provisioned_throughput = {
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
}

# Create the table
response = dynamodb.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput=provisioned_throughput
)

# Wait for the table to be created
dynamodb.get_waiter('table_exists').wait(TableName=table_name)

print("Table created:", response)
