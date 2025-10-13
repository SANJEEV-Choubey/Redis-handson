import redis

def get_redis_stats(redis_host='localhost', redis_port=6379, redis_password=None):
    """Fetch Redis statistics from the INFO command."""
    try:
        # Connect to Redis
        client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        
        # Get persistence and stats info
        info_stats = client.info('stats')
        info_persistence = client.info('persistence')

        # Extract required metrics
        stats = {
            "keyspace_hits": int(info_stats.get("keyspace_hits", 0)),
            "keyspace_misses": int(info_stats.get("keyspace_misses", 0)),
            "total_writes": int(info_stats.get("total_writes_processed", 0)),
            "total_commands": int(info_stats.get("total_commands_processed", 0)),
            "ops_per_sec": int(info_stats.get("instantaneous_ops_per_sec", 1)),  # Avoid division by zero
            "background_writes": int(info_persistence.get("aof_pending_rewrite", 1)),  # Adjust if needed
        }

        return stats

    except redis.RedisError as e:
        print(f"Redis connection error: {e}")
        return None


def calculate_iops(stats):
    """Calculate the required IOPS based on Redis statistics."""
    if not stats:
        return None

    # Avoid division by zero
    ops_per_sec = stats["ops_per_sec"]
    if ops_per_sec == 0:
        raise ValueError("Ops per sec cannot be zero")

    # Calculate uptime in seconds
    uptime_seconds = stats["total_commands"] / ops_per_sec

    # Compute IOPS
    required_iops = ((stats["keyspace_hits"] + stats["keyspace_misses"]) / uptime_seconds) + \
                    (stats["total_writes"] / uptime_seconds) + \
                    stats["background_writes"]

    return round(required_iops, 2)


if __name__ == "__main__":
    # Fetch Redis stats
    redis_stats = get_redis_stats(redis_host='127.0.0.1', redis_port=6379)

    # Calculate IOPS
    if redis_stats:
        iops = calculate_iops(redis_stats)
        print(f"Required IOPS: {iops}")
    else:
        print("Failed to fetch Redis stats.")
