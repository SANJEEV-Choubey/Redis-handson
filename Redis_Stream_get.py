import redis

def handle_stream_messages():
    # Connect to Redis
    redis_conn_str = 'rediss://ibm_cloud_87a7001e_ea39_4679_b19d_4d6d98bced39:xxxxxxxxxx@510533e5-af4b-4bb1-908d-58f62871f8b4.co21lv7d0he2pp3gvq90.dev.databases.appdomain.cloud:31529/0'
    redis_client = redis.from_url(redis_conn_str, ssl_cert_reqs=False)

    # Stream key
    stream_key = 'mystream'

    # Start listening for messages
    last_id = '0'  # Start from the beginning of the stream

    while True:
        try:
            # Use xread to read messages from the stream
            response = redis_client.xread({stream_key: last_id}, block=0)
            
            for stream_name, messages in response:
                for message in messages:
                    last_id, message_data = message
                    decoded_message = {k.decode('utf-8'): v.decode('utf-8') for k, v in message_data.items()}
                    print("Received message:", decoded_message)
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    handle_stream_messages()
