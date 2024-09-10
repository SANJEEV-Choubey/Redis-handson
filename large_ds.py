import sys
import time

def gen_redis_proto(*cmd):
    proto = "*" + str(len(cmd)) + "\r\n"
    for arg in cmd:
        proto += "$" + str(len(arg)) + "\r\n"
        proto += arg + "\r\n"
    return proto

# Adding large lists
large_value = 'x' * 1024  # 1KB string

for n in range(1000000):  # 1 million entries
    sys.stdout.write(gen_redis_proto("LPUSH", "large_list", large_value))
    time.sleep(0.01)  # Add a short sleep to reduce pressure on the pipe