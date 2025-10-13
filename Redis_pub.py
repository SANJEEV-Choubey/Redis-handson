import redis

def publish_message():
    # Connect to Redis Server
    # Modify Redis connection string as needed
    redis_conn_str = 'rediss://ibm_cloud_b6422a91_9f31_49d7_a29f_ca46ceeaa48e:xxxxxxxxxxxxxxxxxxx@a6e221b4-1a96-407d-b522-1fddd80cb314.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:32667/0'
        # Create a connection pool
    redis_pool = redis.ConnectionPool.from_url(redis_conn_str, ssl_ca_certs="/Users/sanjeevchoubey/Downloads/e0dc3caf-a1f2-11e9-b619-02c049fdd00c")
    redis_client = redis.Redis(connection_pool=redis_pool)
    
    # Publish some messages
    redis_client.publish('channel', 'Hello, world!')
    redis_client.publish('channel', 'This is a Redis Pub/Sub demo.')
    redis_client.publish('channel', 'Goodbye!')

if __name__ == "__main__":
    publish_message()
