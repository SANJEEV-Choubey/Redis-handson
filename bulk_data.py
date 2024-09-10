import sys

# Function to generate Redis protocol
def gen_redis_proto(*cmd):
    """
    This function generates the Redis protocol for a given command.
    """
    proto = "*"+str(len(cmd))+"\r\n"
    for arg in cmd:
        proto += "$"+str(len(arg))+"\r\n"
        proto += arg+"\r\n"
    return proto

# Calculate approximate key-value size needed
# Number of keys: 50,331,671
# To reach 28 GB, each value needs to be around 600 bytes
value_size = 600  # Adjust the size to fit your target

# Function to generate a random value string of a given size
def generate_value(size):
    return 'A' * size  # Simple repetitive string

# Looping over the range of keys and writing Redis protocol to stdout
for n in range(50331671):
    key = f"Key{n}"
    value = generate_value(value_size)
    
    # Writing to stdout the Redis protocol for the SET command with the key and value
    sys.stdout.write(gen_redis_proto("SET", key, value))

    # Optional: Print progress every 1 million keys
    if n % 1000000 == 0:
        print(f"Inserted {n} keys so far...")
