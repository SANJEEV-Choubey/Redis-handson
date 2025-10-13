import redis

def execute_lua_script():
    # Connect to Redis Server
    # Modify Redis connection string as needed
    redis_conn_str = 'rediss://ibm_cloud_b6422a91_9f31_49d7_a29f_ca46ceeaa48e:xxxxxxxxxxxxxxxxxxxxxxx@a6e221b4-1a96-407d-b522-1fddd80cb314.a618efcd6c3341158fb843970f0d7edd.databases.appdomain.cloud:32667/0'
    # Create a connection pool
    redis_pool = redis.ConnectionPool.from_url(redis_conn_str, ssl_ca_certs="/Users/sanjeevchoubey/Downloads/e0dc3caf-a1f2-11e9-b619-02c049fdd00c")
    redis_client = redis.Redis(connection_pool=redis_pool)
    # Define a Lua script
    lua_script = """
    local key = KEYS[1]
    local value = ARGV[1]
    redis.call("SET", key, value)
    return redis.call("GET", key)
    """

    # Execute the Lua script
    try:
        key = "test_key"
        value = "Hello, Redis!"
        result = redis_client.eval(lua_script, 1, key, value)
        print(f"Result from Lua script: {result}")
    except Exception as e:
        print(f"Error executing Lua script: {e}")

if __name__ == "__main__":
    execute_lua_script()
