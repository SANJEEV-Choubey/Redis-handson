
import sys
import redis
from urllib.parse import urlparse
import time
user='admin'
password='xxxxxxxx'
hostname='e957bedd-59dc-4ca1-9efd-4b15aa65b0a0.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud'
port='31484'
ssl_ca_certs='/Users/sanjeevchoubey/Downloads/preproduction-skc'

password1='xxxxxxxxx'
hostname1='ed8a9748-ad54-4361-90ee-ec4585d659df.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud'
port1= '31604'
ssl_ca_certs1='/Users/sanjeevchoubey/Downloads/preproduction-skc1'


header = ['firstname', 'lastname','fullname', 'address']

def conn():
    try:
        # r = redis.StrictRedis(
        #     host='rediss://skc-redis.cbm2prkd0olp4tad867g.dev.databases.appdomain.cloud',
        #     port=32329,
        #     decode_responses=True,
        #     db=0,
        #     username='default',
        #     password='PwFElb'
        #     )
        # parsed = urlparse(connection_string)
        # connection_string='rediss://admin:databasesforredis@ed8a9748-ad54-4361-90ee-ec4585d659df.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud:31604/0'
        # parsed = urlparse(connection_string)
        # r = redis.StrictRedis(
        #     host="rediss://skc-redis62new.cbm2prkd0olp4tad867g.dev.databases.appdomain.cloud",
        #     port="31030",
        #     password="JFPFcZ",
        #     #username="default",
        #     db=0,
        #     ssl=True,
        #     #tls=True,
        #     #tlsAllowInvalidCertificates=True,
        #     ssl_ca_certs='/Users/sanjeevchoubey/go/src/github.ibm.com/SANJEEV-Choubey/Redis-handson/ca-cert.crt',
        #     decode_responses=True)
        #connection_string = 'rediss://admin:databasesforredis@ed8a9748-ad54-4361-90ee-ec4585d659df.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud:31604/0',
        # password='redisfordatabases',
        #parsed = urlparse(connection_string)
        r = redis.StrictRedis(
            host='e957bedd-59dc-4ca1-9efd-4b15aa65b0a0.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud',
            port='31484',
            username='admin',
            password='redisfordatabases',
            ssl=True,
            ssl_ca_certs='/Users/sanjeevchoubey/Downloads/preproduction-skc',
            db=0,
            decode_responses=True)
        print("ping")
        print(r.ping())
        return r
    except Exception as e:
        print(e)
        print(r)
        sys.exit("error in connection..")


def conn1():
    try:
        r = redis.StrictRedis(
            host='ed8a9748-ad54-4361-90ee-ec4585d659df.bn5hbied0ao9rn2ced1g.databases.appdomain.cloud',
            port='31604',
            username='admin',
            password='redisfordatabases',
            ssl=True,
            ssl_ca_certs='/Users/sanjeevchoubey/Downloads/preproduction-skc1',
            db=0,
            decode_responses=True)
        print("ping1")
        print(r.ping())
        return r
    except Exception as e:
        print(e)
        print(r)
        sys.exit("error in connection1..")


def get_values(r,key):
    key=str(key)
    try:
        value= r.get(key)
    except Exception as e:
        print(e)
        sys.exit("error in execution..")
    return value


def set_values(r,key,value):
    key=str(key)
    try:
        r.set(key,value)
    except Exception as e:
        print(e)
        sys.exit("error in setting values..")
    print("value inserted successfully....")


def uptime(r,r1):
    while True:
        # get uptime for redis1
        redis1_info = r.info()
        redis1_uptime = redis1_info['uptime_in_seconds']

        # get uptime for redis2
        redis2_info = r1.info()
        redis2_uptime = redis2_info['uptime_in_seconds']

        # print uptime for both instances
        print(f"Redis1 uptime: {redis1_uptime}s")
        print(f"Redis2 uptime: {redis2_uptime}s")

        # wait for 10 seconds before checking again
        time.sleep(10)

def downtime(r,r1):
    # Loop indefinitely
    while True:
        # Check if Redis instance is reachable
        try:
            r.ping()
            print('Redis is up and running!')

        except redis.exceptions.ConnectionError:
            print('Error: Redis instance is not reachable')
            # Log the downtime timestamp
            with open('redis_downtime.log', 'a') as f:
                f.write(f'{time.time()}\n')

        # Check if Redis instance is reachable
        try:
            r1.ping()
            print('Redis1 is up and running!')

        except redis.exceptions.ConnectionError:
            print('Error: Redis1 instance is not reachable')
            # Log the downtime timestamp
            with open('redis_downtime1.log', 'a') as f:
                f.write(f'{time.time()}\n')

        # Wait for 5 seconds before the next check
        time.sleep(5)

print("create connection")
r=conn()
r1=conn1()
# r.ping()
print("Set values")
key='IN'
value='India'
set_values(r,key,value)
set_values(r1,key,value)
kkey='US'
value='USA'
set_values(r,key,value)
set_values(r1,key,value)
print("Get values")
print(get_values(r,'IN'))
print(get_values(r1,'IN'))
# uptime(r,r1)
downtime(r,r1)



