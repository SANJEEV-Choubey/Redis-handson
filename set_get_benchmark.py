import redis
import time
from concurrent.futures import ThreadPoolExecutor

# Function to perform SET operations
def perform_set_operations(redis_client, num_iterations):
    # Perform SET operations
    for i in range(num_iterations):
        # Example operation: Set a key-value pair
        redis_client.set(f'key_{i}', f'value_{i}')

# Function to perform GET operations
def perform_get_operations(redis_client, num_iterations):
    # Perform GET operations
    for i in range(num_iterations):
        # Example operation: Get the value for a key
        redis_client.get(f'key_{i}')

# Main function for benchmarking SET and GET operations
def benchmark(redis_client, num_connections, num_iterations_per_connection):
    start_time = time.time()

    # Create a ThreadPoolExecutor to manage multiple connections
    with ThreadPoolExecutor(max_workers=num_connections) as executor:
        # Submit SET tasks to the executor
        set_futures = [executor.submit(perform_set_operations, redis_client, num_iterations_per_connection) for _ in range(num_connections)]

        # Submit GET tasks to the executor
        get_futures = [executor.submit(perform_get_operations, redis_client, num_iterations_per_connection) for _ in range(num_connections)]
        
        # Wait for all tasks to complete
        for future in set_futures + get_futures:
            future.result()

    end_time = time.time()
    total_time = end_time - start_time

    print(f'Total time taken for {num_connections} connections: {total_time} seconds')

# Test parameters
redis_conn_str = 'rediss://user:xxxxxx@a37b1b4b-f3a7-4fdf-a3e9-7865dfee840e.cg91ppcd0kqqkou6l940.dev.databases.appdomain.cloud:31400/0'
redis_client = redis.from_url(redis_conn_str, ssl_cert_reqs=False)
num_connections = 100000
num_iterations_per_connection = 100000

# Perform benchmarking for SET and GET operations
print("Benchmarking SET operations:")
benchmark(redis_client, num_connections, num_iterations_per_connection)

# Wait for a while before benchmarking GET operations
time.sleep(2)

print("Benchmarking GET operations:")
benchmark(redis_client, num_connections, num_iterations_per_connection)



