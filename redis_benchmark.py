import redis
import time
from concurrent.futures import ThreadPoolExecutor

# Function to perform Redis operations
def perform_redis_operations(redis_client, num_iterations):
    # Perform Redis operations
    for i in range(num_iterations):
        # Example operation: Set a key-value pair
        redis_client.set(f'key_{i}', f'value_{i}')

# Main function for benchmarking
def benchmark(redis_client, num_connections, num_iterations_per_connection):
    start_time = time.time()

    # Create a ThreadPoolExecutor to manage multiple connections
    with ThreadPoolExecutor(max_workers=num_connections) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(perform_redis_operations, redis_client, num_iterations_per_connection) for _ in range(num_connections)]
        
        # Wait for all tasks to complete
        for future in futures:
            future.result()

    end_time = time.time()
    total_time = end_time - start_time

    print(f'Total time taken for {num_connections} connections: {total_time} seconds')

# Test parameters
redis_conn_str = 'rediss://ibm_cloud_04e9ddc0_f8ba_4d3d_a184_078c23d0234f:xxxxxxxxx@ebf44a4e-5311-45f1-8b0d-261e818dc200.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:32206/0'
redis_client = redis.from_url(redis_conn_str, ssl_ca_certs="/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001")
num_connections = 100000
num_iterations_per_connection = 1000

# Perform benchmarking
benchmark(redis_client, num_connections, num_iterations_per_connection)
