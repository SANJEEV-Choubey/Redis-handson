import redis

def publish_messages():
    # Connect to Redis
    redis_conn_str = 'rediss://ibm_cloud_87a7001e_ea39_4679_b19d_4d6d98bced39:xxxxxxxxx@510533e5-af4b-4bb1-908d-58f62871f8b4.co21lv7d0he2pp3gvq90.dev.databases.appdomain.cloud:31529/0'
    redis_client = redis.from_url(redis_conn_str, ssl_cert_reqs=False)

    # Stream key
    stream_key = 'mystream'

    # Publish messages to the stream
    for i in range(10):
        message = {'field1': f'value{i}', 'field2': f'value{i+1}'}
        redis_client.xadd(stream_key, message)
        print(f"Published message: {message}")

if __name__ == "__main__":
    publish_messages()
