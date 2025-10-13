import redis

def calculate_cow_factor(redis_host='localhost', redis_port=6379, redis_password=None):
    try:
        client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

        # Fetch memory and persistence info
        memory_info = client.info('memory')
        persistence_info = client.info('persistence')

        # Get values
        used_memory = int(memory_info.get('used_memory', 0))
        rdb_cow_size = int(persistence_info.get('rdb_last_cow_size', 0))
        aof_cow_size = int(persistence_info.get('aof_last_cow_size', 0))

        # Compute CoW Factors
        rdb_cow_factor = (rdb_cow_size / used_memory) if used_memory > 0 else 0
        aof_cow_factor = (aof_cow_size / used_memory) if used_memory > 0 else 0

        print(f"RDB CoW Factor: {rdb_cow_factor:.2%}")
        print(f"AOF CoW Factor: {aof_cow_factor:.2%}")

        return rdb_cow_factor, aof_cow_factor

    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Example Usage
if __name__ == "__main__":
    calculate_cow_factor()
