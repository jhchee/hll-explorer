import time

import bson
import redis

try:
    rc = redis.StrictRedis(host='localhost', port=6379, db=0)
    start_time = time.perf_counter()
    for _ in range(1, 1000):
        id = bson.ObjectId().__str__()
        rc.execute_command(f"pfadd visitor_2023_07_01 {id}")
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f'Function Took {total_time:.4f} seconds')
    res = rc.execute_command("pfcount visitor_2023_07_01")
    print(res)

except redis.ConnectionError as e:
    print(f"Error: {e}")
