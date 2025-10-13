import redis

def handle_messages():
    # Connect to Redis
    redis_conn_str = 'rediss://ibm_cloud_b6422a91_9f31_49d7_a29f_ca46ceeaa48e:xxxxxxxxxxxx@a6e221b4-1a96-407d-b522-1fddd80cb314.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:32667/0'
        # Create a connection pool
    redis_pool = redis.ConnectionPool.from_url(redis_conn_str, ssl_ca_certs="/Users/sanjeevchoubey/Downloads/e0dc3caf-a1f2-11e9-b619-02c049fdd00c")
    redis_client = redis.Redis(connection_pool=redis_pool)
    
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