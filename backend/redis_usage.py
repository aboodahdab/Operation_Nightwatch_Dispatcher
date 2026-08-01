import redis
import json

# decode_responses=True means you get str back instead of bytes
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def dump_data_into_redis(data):

    
    print(data,type(data), "redis one though", )
    r.xadd("data", data)

