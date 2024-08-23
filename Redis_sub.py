import redis

def handle_messages():
    # Connect to Redis
    redis_conn_str = 'rediss://ibm_cloud_87a7001e_ea39_4679_b19d_4d6d98bced39:f08c3258c74470f90decc01084c0e3a08dd1b23821053f8fe53d550997c5a9d1@510533e5-af4b-4bb1-908d-58f62871f8b4.co21lv7d0he2pp3gvq90.dev.databases.appdomain.cloud:31529/0'
    redis_client = redis.from_url(redis_conn_str,ssl_cert_reqs=False)
    
    # Create a Pub/Sub instance
    pubsub = redis_client.pubsub()
    
    # Subscribe to a channel
    pubsub.subscribe('channel')
    
    # Start listening for messages
    for message in pubsub.listen():
        if message['type'] == 'message':
            print("Received message:", message['data'].decode('utf-8'))

if __name__ == "__main__":
    handle_messages()