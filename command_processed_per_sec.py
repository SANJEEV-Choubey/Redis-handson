import redis
import time

def measure_commands_per_second(redis_host='localhost', redis_port=6379, redis_password=None, interval=5):
    """
    Measures how many commands are processed per second.
    
    :param redis_host: Redis server hostname or IP.
    :param redis_port: Redis server port.
    :param redis_password: Redis password (if required).
    :param interval: Time interval (seconds) to measure.
    """
    try:
        client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

        # Get initial value
        stats1 = client.info('stats')
        commands1 = int(stats1.get('total_commands_processed', 0))
        
        time.sleep(interval)  # Wait for interval
        
        # Get value after interval
        stats2 = client.info('stats')
        commands2 = int(stats2.get('total_commands_processed', 0))

        # Calculate commands per second
        commands_per_sec = (commands2 - commands1) / interval
        print(f"Commands per second: {commands_per_sec:.2f}")
        return commands_per_sec

    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

# Example usage
if __name__ == "__main__":
    measure_commands_per_second(redis_host='localhost', redis_port=6379, redis_password=None, interval=5)
