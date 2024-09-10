# Importing the sys module to use the stdout.write function
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

# Looping over the range of 50331671 to generate 1.5 gb of data
for n in range(50331671):
    # Writing to stdout the Redis protocol for the SET command with the given key and value
    sys.stdout.write(gen_redis_proto("SET", f"Key{n}", f"Value{n}"))

