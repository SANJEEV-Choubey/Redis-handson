import redis

def calculate_iops(redis_host='localhost', redis_port=6379, redis_password=None, cow_factor=3, snapshot_interval=60):
    """
    Connects to Redis, retrieves INFO persistence stats, and calculates required IOPS.
    
    :param redis_host: Redis server hostname or IP.
    :param redis_port: Redis server port.
    :param redis_password: Redis password (if required).
    :param cow_factor: Copy-on-Write overhead factor (default: 3 for HDD).
    :param snapshot_interval: RDB snapshot interval in seconds (default: 60s).
    :return: Required IOPS for RDB snapshots.
    """
    try:
        # Connect to Redis
        client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        
        # Fetch persistence stats
        info_persistence = client.info('persistence')

        # Get changes since last RDB save
        changes_since_last_save = int(info_persistence.get('rdb_changes_since_last_save', 0))

        # Calculate required IOPS
        required_iops = (changes_since_last_save * cow_factor) / snapshot_interval

        print(f"Changes since last save: {changes_since_last_save}")
        print(f"Required IOPS (with CoW Factor {cow_factor}): {required_iops:.2f}")
        return required_iops

    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

# Example usage
if __name__ == "__main__":
    calculate_iops(redis_host='localhost', redis_port=6379, redis_password=None)
