from azure.cosmos import CosmosClient, PartitionKey

# Initialize Cosmos DB client
endpoint = "https://emotiguard-database.documents.azure.com:443/"
key = "j4sZto9VEgTVKvuFDpPGtWQBTla5DcvTd4YcLNSZUo7R9ZAcJKcM7dLYWhWjYWPTzChiTTLitFQCACDblM4Gfw=="
client = CosmosClient(endpoint, key)

# Define your database and container names
database_name = "emotiguard_db"
container_name = "User_container"

# Define your container definition
container_definition = {
    "id": container_name,
    "partition_key": PartitionKey(
        path="/id_token"
    ),  # Specify id_token as the partition key
}

# Get or create the database
database = client.create_database_if_not_exists(id=database_name)

# Create the container if it doesn't exist
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=container_definition["partition_key"],
    offer_throughput=400,
)

# Example data to be inserted
sample_data = [
    {
        "id": "1",
        "id_token": "token1",
        "email": "user1@example.com",
        "user_id": "user1",
    },
    {"id": "2", "id_token": "token2", "email": "user2@example.com", "user_id": "user2"},
    # Add more sample data as needed
]
# Insert sample data into the container
for data in sample_data:
    container.create_item(body=data)

print("Container with partition key 'id_token' created and sample data added.")
