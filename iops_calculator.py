

def calculate_iops(keyspace_hits, keyspace_misses, total_writes, total_commands, ops_per_sec, background_writes=1):
    # Avoid division by zero
    if ops_per_sec == 0:
        raise ValueError("Ops per sec cannot be zero")

    # Calculate uptime in seconds
    uptime_seconds = total_commands / ops_per_sec

    # Calculate required IOPS
    required_iops = ((keyspace_hits + keyspace_misses) / uptime_seconds) + (total_writes / uptime_seconds) + background_writes
    
    return round(required_iops, 2)


# Example usage with your Redis stats
redis_stats = {
    "keyspace_hits": 11182658,
    "keyspace_misses": 6273790,
    "total_writes": 40254842,x
    "total_commands": 23091673,
    "ops_per_sec": 151,
    "background_writes": 1  # Adjust based on AOF settings
}

iops = calculate_iops(**redis_stats)
print(f"Required IOPS: {iops}")
