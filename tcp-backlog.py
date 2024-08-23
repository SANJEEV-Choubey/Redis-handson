import redis
import time

def track_tcp_backlog(redis_client, interval=5):
    # Connect to Redis

    # Main loop
    while True:
        # Get server information using the INFO command
        server_info = redis_client.info("server")

        # Extract and print the tcp_backlog value
        tcp_backlog = server_info.get('tcp_backlog', 'N/A')
        print(f"Current tcp_backlog value: {tcp_backlog}")

        # Wait for the specified interval before checking again
        time.sleep(interval)

# Test parameters
redis_conn_str = 'rediss://user:xxxxxx@a37b1b4b-f3a7-4fdf-a3e9-7865dfee840e.cg91ppcd0kqqkou6l940.dev.databases.appdomain.cloud:31400/0'
redis_client = redis.from_url(redis_conn_str, ssl_cert_reqs=False)
update_interval = 5  # Update interval in seconds

# Start tracking tcp_backlog value
track_tcp_backlog(redis_client, update_interval)
