import redis

def fetch_redis_command_calls(redis_pool):
    """
    Fetch the number of calls for each Redis command.
    """
    try:
        r = redis.Redis(connection_pool=redis_pool)
        commandstats = r.info("commandstats")  # Fetch only commandstats section
        
        # Extract and return a dictionary with command -> number of calls
        command_calls = {cmd: stats["calls"] for cmd, stats in commandstats.items()}
        return command_calls

    except Exception as e:
        print(f"Error fetching Redis commandstats: {e}")
        return None

if __name__ == "__main__":
    # Modify Redis connection string as needed
    redis_conn_str = 'rediss://ibm_cloud_fba768c6_4fc9_4168_87db_8897c3f8499c:xxxxxxxxxxxxx@2001266c-9717-42c1-8a8f-e34cfff59e24.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:31029/0'
    
    # Create a connection pool with SSL certificates
    redis_pool = redis.ConnectionPool.from_url(
        redis_conn_str, ssl_ca_certs="/Users/sanjeevchoubey/Downloads/e0dc3caf-a1f2-11e9-b619-02c049fdd00c"
    )

    command_calls = fetch_redis_command_calls(redis_pool)

    if command_calls:
        print("Redis Command Calls:")
        for command, calls in command_calls.items():
            print(f"{command}: {calls}")
