import redis

def publish_message():
    # Connect to Redis Server
    # Modify Redis connection string as needed
    redis_conn_str = 'rediss://ibm_cloud_87a7001e_ea39_4679_b19d_4d6d98bced39:f08c3258c74470f90decc01084c0e3a08dd1b23821053f8fe53d550997c5a9d1@510533e5-af4b-4bb1-908d-58f62871f8b4.co21lv7d0he2pp3gvq90.dev.databases.appdomain.cloud:31529/0'
    redis_client = redis.from_url(redis_conn_str,ssl_cert_reqs=False)
    
    # Publish some messages
    redis_client.publish('channel', 'Hello, world!')
    redis_client.publish('channel', 'This is a Redis Pub/Sub demo.')
    redis_client.publish('channel', 'Goodbye!')

if __name__ == "__main__":
    publish_message()
