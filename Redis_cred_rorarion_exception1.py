import redis
import time
import threading
from datetime import datetime

# Redis configuration
# REDIS_CONN_STR = 'rediss://ibm_cloud_ee1aab80_5c03_445b_b319_be9dbad862fd:xxxxxxxxxxxxxxxx@90b8bbc1-fb39-4a12-a72e-128d90247303.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:31116/0'
# SSL_CA_CERTS = "/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001"
# REDIS_CONN_STR = 'rediss://ibm_cloud_44217022_cef2_4d62_b639_3b3a8063fb27:xxxxxxxxxxxxxxx@1e7e5a2c-bc2d-4425-a6ad-5a4086ae64d3.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30511/0'
# SSL_CA_CERTS ='/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001'

REDIS_CONN_STR = 'rediss://ibm_cloud_89c59164_8294_49c4_b776_3c68d7248575:xxxxxxxxxxxxxxx@2be0d6bd-412b-422d-b8e3-cfde9c4a1bfb.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:32717/0'
SSL_CA_CERTS = '/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001'
TOTAL_CONNECTIONS = 2000


# Function to keep each connection active
def redis_worker(index):
    client = redis.Redis.from_url(REDIS_CONN_STR, ssl_ca_certs=SSL_CA_CERTS)
    key = f"worker_key_{index}"
    value = f"worker_value_{index}"

    while True:
        try:
            client.set(key, value)
            client.get(key)
            time.sleep(10)  # Prevent excessive CPU usage
        except Exception as e:
            print(f"Client {index}: Error - {e}")
            break

# Create 210 threads, each maintaining an active Redis connection
threads = []
for i in range(TOTAL_CONNECTIONS):
    t = threading.Thread(target=redis_worker, args=(i,))
    t.daemon = True  # Allow graceful exit on script termination
    t.start()
    threads.append(t)

# Monitor connections
while True:
        try:
            redis_client = redis.Redis.from_url(REDIS_CONN_STR, ssl_ca_certs=SSL_CA_CERTS)
            info = redis_client.info('clients')
            connected_clients = info.get("connected_clients", 0)
            print(f"Connected Clients: {connected_clients} at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        except Exception as e:
            print(f"Error fetching connected clients: {e}")
        
        time.sleep(1)  # Check every 10 seconds