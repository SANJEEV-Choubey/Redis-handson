
import redis

# Modify Redis connection string as needed
redis_conn_str = 'rediss://ibm_cloud_71187013_80c3_41a5_8898_540d5d8d8c21:e50e9c18361d302f631bae15e258bfadf304f5c653b7b197da81d08fcada252e@557b7251-0f7c-4251-8ca6-821ae26eeb18.c5km1ted03t0e8geevf0.databases.appdomain.cloud:30319/0'
# Connect to Redis server
r = redis.from_url(redis_conn_str,ssl_ca_certs="/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001")

# Set a key-value pair
r.set('key1', 'value1')

# Get the value of a key
value = r.get('key1')
print("Value of key1:", value.decode('utf-8'))

# Check if a key exists
if r.exists('key1'):
    print("Key 'key1' exists")
else:
    print("Key 'key1' does not exist")

# Increment a key's value
r.incr('counter')
print("Counter value:", r.get('counter').decode('utf-8'))

# Delete a key
r.delete('key1')

# Check again if the key exists
if r.exists('key1'):
    print("Key 'key1' exists")
else:
    print("Key 'key1' does not exist")