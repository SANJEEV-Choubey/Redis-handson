
def gen_redis_proto(*cmd):
    proto = "*" + str(len(cmd)) + "\r\n"
    for arg in cmd:
        proto += "$" + str(len(arg)) + "\r\n"
        proto += arg + "\r\n"
    return proto

# Generate a large value (1MB)
large_value = 'x' * 1024 * 1024  # 1MB string

# Write the Redis commands to a file
with open("/tmp/redis_commands.txt", "w") as f:
    for n in range(1500):
        f.write(gen_redis_proto("SET", f"Key{n}", large_value))
