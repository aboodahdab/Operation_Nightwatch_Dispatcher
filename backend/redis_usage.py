import redis
import json

# decode_responses=True means you get str back instead of bytes

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def dump_data_into_redis(data):

    print("Dumping data into Redis:")
    r.xadd("data", data ,maxlen=170,approximate=False)
 