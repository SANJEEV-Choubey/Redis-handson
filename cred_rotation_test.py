import redis
import time
import threading
from datetime import datetime

# Redis configuration
# REDIS_CONN_STR = 'rediss://ibm_cloud_a582e710_71ed_4425_8f1c_dd215141e86c:xxxxxxxxxxxxxxxxx@b505964f-ebe2-497d-bd02-b29502daf3bf.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30891/0'
# REDIS_CONN_STR = 'rediss://ibm_cloud_5892e49f_0e63_4ad7_aa7d_978cae29cc86:xxxxxxxxxxxxxxxx@8bacc194-fc57-401e-9f59-12a7b1642330.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:32426/0'
# SSL_CA_CERTS = "/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001"
# REDIS_CONN_STR = 'rediss://ibm_cloud_d5c44717_f4d2_465c_baf6_307e4616e688:xxxxxxxxxxxx@64e2733a-9db3-49bc-aa77-5dcc6e0d7cb7.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30709/0'
# SSL_CA_CERTS ='/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001'
TOTAL_CONNECTIONS = 2000
REDIS_CONN_STR = 'rediss://ibm_cloud_90d7fcb6_d658_4fdb_abfa_aae4d3a94433:xxxxxxxxxxxxxxxx@e751e6e7-d4d0-4991-b9d9-060319a886d2.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud:30093/0'
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