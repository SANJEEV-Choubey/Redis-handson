import redis
import time
import threading
from datetime import datetime

# Redis configuration
# REDIS_CONN_STR = 'rediss://ibm_cloud_172eff45_bff2_4589_951e_69999d0acd60:xxxxxxxxxxxxxxxxxxx@1f9fb872-76f9-44c9-92a1-618f1da1ee85.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:32646/0'
# SSL_CA_CERTS = "/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001"
# REDIS_CONN_STR = 'rediss://ibm_cloud_44217022_cef2_4d62_b639_3b3a8063fb27:xxxxxxxxxxxxxxx@1e7e5a2c-bc2d-4425-a6ad-5a4086ae64d3.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30511/0'
# SSL_CA_CERTS ='/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001'
# REDIS_CONN_STR = 'rediss://ibm_cloud_baa8b8e4_8c9a_471b_9d8e_d8b09d156b56:xxxxxxxxxxxxxxx@f665de68-e3b9-4a24-9913-5be0fa59475b.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud:31045/0'
# SSL_CA_CERTS = '/Users/sanjeevchoubey/Downloads/f9b375e4-06fe-11ea-91a0-8680a41a8aef'
TOTAL_CONNECTIONS = 2000
# REDIS_CONN_STR = "rediss://ibm_cloud_1b22fc60_62f1_42c4_89bf_03b17e5a915c:xxxxxxxxxxxx@2001266c-9717-42c1-8a8f-e34cfff59e24.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:31029/0"
# SSL_CA_CERTS = '/Users/sanjeevchoubey/Downloads/e0dc3caf-a1f2-11e9-b619-02c049fdd00c'

REDIS_CONN_STR = 'rediss://ibm_cloud_90d7fcb6_d658_4fdb_abfa_aae4d3a94433:xxxxxxxxxxxxxxx@e751e6e7-d4d0-4991-b9d9-060319a886d2.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud:30093/0'
SSL_CA_CERTS = '/Users/sanjeevchoubey/Downloads/f9b375e4-06fe-11ea-91a0-8680a41a8aef'


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