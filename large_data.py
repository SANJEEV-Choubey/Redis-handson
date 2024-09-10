import redis
import random
import string
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Insert data into Redis.')
parser.add_argument('--host', default='localhost', help='Redis host')
parser.add_argument('--port', type=int, default=6379, help='Redis port')
parser.add_argument('--user', help='Redis username')
parser.add_argument('--pass', help='Redis password')

args = parser.parse_args()

# Connect to Redis
try:
    # Connect with username and password if provided
    r = redis.Redis(host=args.host, port=args.port, username=args.user, password=args.pass, decode_responses=True)
    # Test the connection
    r.ping()
    print("Connected to Redis successfully")
except redis.AuthenticationError as e:
    print(f"Authentication failed: {e}")
    exit(1)
except redis.ConnectionError as e:
    print(f"Connection failed: {e}")
    exit(1)

def generate_random_string(size=1024):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

# Insert a large number of keys
for i in range(10**6):  # Adjust this number based on desired data size
    key = f'key:{i}'
    value = generate_random_string(size=1024)  # Adjust size as needed
    try:
        r.set(key, value)
        if i % 10000 == 0:
            print(f'Inserted {i} keys')
    except redis.RedisError as e:
        print(f"Error inserting key {key}: {e}")
        exit(1)

print('Data insertion complete')
