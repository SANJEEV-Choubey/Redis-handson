import redis
import time
from concurrent.futures import ThreadPoolExecutor

# Redis configuration
# REDIS_CONN_STR = 'rediss://ibm_cloud_94132c2d_6526_43a9_bd6c_280f5d409cac:xxxxxxxxxxxxx@c6682a7c-f8fc-4705-bdfe-c155e5db39c9.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:31465/0'
# SSL_CA_CERTS = "/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001"
REDIS_CONN_STR = 'rediss://ibm_cloud_f9b8e7d5_c92a_4ec6_833e_ea55491629ee:xxxxxxxxxxxxxxxx@fa9c2c1e-1cf2-43ab-a5e3-b19c95645ccd.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30764/0'
SSL_CA_CERTS ='/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001'
TOTAL_CONNECTIONS = 2000

def create_redis_pool():
    return redis.ConnectionPool.from_url(REDIS_CONN_STR, max_connections=TOTAL_CONNECTIONS, ssl_ca_certs=SSL_CA_CERTS)

redis_pool = create_redis_pool()

def create_clients():
    return [redis.Redis(connection_pool=redis_pool) for _ in range(TOTAL_CONNECTIONS)]

clients = create_clients()

def redis_operations(client, index):
    key = f"test_key_{index}"
    value = f"test_value_{index}"
    
    try:
        client.set(key, value)
        read_value = client.get(key)
        print(f"Client {index}: Wrote {value}, Read {read_value.decode()}")
    except (redis.ConnectionError, redis.TimeoutError) as e:
        print(f"Client {index}: Connection error - {e}. Reconnecting...")
        time.sleep(1)
        client = redis.Redis(connection_pool=create_redis_pool())
    except Exception as e:
        print(f"Client {index}: Error - {e}")

def worker(index):
    while True:
        try:
            redis_operations(clients[index], index)
            redis_client = redis.Redis(connection_pool=redis_pool)
            info = redis_client.info('clients')
            connected_clients = info.get("connected_clients", 0)
            print("==========================================================================")
            print(f"Active Redis Connections: {connected_clients}")
            print("==========================================================================")
            time.sleep(10)
        except Exception as e:
            print(f"Worker {index}: Unexpected error - {e}")
            time.sleep(5)

# Using ThreadPoolExecutor for better management
with ThreadPoolExecutor(max_workers=2000) as executor:
    for i in range(TOTAL_CONNECTIONS):
        executor.submit(worker, i)

print("All clients are connected and performing operations.")

# Monitoring Redis connected clients
while True:
    try:
        redis_client = redis.Redis(connection_pool=redis_pool)
        info = redis_client.info('clients')
        connected_clients = info.get("connected_clients", 0)
        print("==========================================================================")
        print(f"Active Redis Connections: {connected_clients}")
        print("==========================================================================")
    except Exception as e:
        print(f"Error fetching connected clients: {e}")
    time.sleep(60)
