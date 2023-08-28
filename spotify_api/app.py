import boto3

# Create a session with specified region
session = boto3.Session(region_name='eu-central-1')

# Get credentials from the session
credentials = session.get_credentials()

# Print out the information
print("Region:", session.region_name)
print("Access Key:", credentials.access_key)
print("Secret Key:", credentials.secret_key)

