import sys
import time

def gen_redis_proto(*cmd):
    proto = "*" + str(len(cmd)) + "\r\n"
    for arg in cmd:
        proto += "$" + str(len(arg)) + "\r\n"
        proto += arg + "\r\n"
    return proto

# Generating large values
large_value = 'x' * 1024 * 1024  # 1MB string

for n in range(1500):  # 1500 * 1MB = 1.5GB
    sys.stdout.write(gen_redis_proto("SET", f"Key{n}", large_value))
    time.sleep(0.01)  # Add a short sleep to reduce pressure on the pipe