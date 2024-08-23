import redis
import matplotlib.pyplot as plt

def fetch_redis_info(redis_pool):
    """
    Fetch Redis INFO command data using a connection pool.
    """
    try:
        r = redis.Redis(connection_pool=redis_pool)
        info = r.info()
        return info
    except Exception as e:
        print(f"Error fetching Redis info: {e}")
        return None

def create_dashboard(info):
    """
    Create a simple dashboard to visualize Redis INFO data.
    """
    if info is None:
        print("Cannot create dashboard. Redis info is not available.")
        return
    
    # Extract relevant data for visualization
    memory_data = {
        'used_memory': info['used_memory'],
        'used_memory_rss': info['used_memory_rss'],
        'used_memory_peak': info['used_memory_peak'],
        'used_memory_lua': info['used_memory_lua']
    }
    commands_processed = {
        'total_commands_processed': info['total_commands_processed'],
        'instantaneous_ops_per_sec': info['instantaneous_ops_per_sec']
    }
    
    connected_clients = {
        'connected_clients': info['connected_clients'],
        'maxclients': info['maxclients']
    }

    # Plot memory data
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.bar(memory_data.keys(), memory_data.values(), color=['blue', 'green', 'red', 'orange'])
    plt.title('Memory Usage')
    plt.ylabel('Memory (bytes)')
    plt.xticks(rotation=45)
    
    # Plot commands processed data
    plt.subplot(1, 3, 2)
    plt.bar(commands_processed.keys(), commands_processed.values(), color=['purple', 'cyan'])
    plt.title('Commands Processed')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # Plot connected clients data
    plt.subplot(1, 3, 3)
    plt.bar(connected_clients.keys(), connected_clients.values(), color=['purple', 'cyan'])
    plt.title('Connected Clients')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Modify Redis connection string as needed, For simplicity and demo, it has been added here
    redis_conn_str = 'rediss://ibm_cloud_dc5af8d9_80ce_4a67_b3da_185ec8d49e60:xxxxxxxxxx@c3834e0d-be16-43f2-9bed-158a371eb3ea.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30837/0'
    
    # Create a connection pool
    redis_pool = redis.ConnectionPool.from_url(redis_conn_str, ssl_ca_certs="/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001")

    info = fetch_redis_info(redis_pool)
    create_dashboard(info)
