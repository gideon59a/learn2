import redis

from constants import redis_ip  # '172.18.122.195

rdb0 = redis.Redis(host=redis_ip, port=6379, db=0)  # password='password')
rdb1 = redis.Redis(host=redis_ip, port=6379, db=1)  # password='password')

rdb0.set('foo0', 'bar0')  # key type string
value = rdb0.get('foo0')
print(value)

rdb1.set('foo1', 'bar1')
value = rdb1.get('foo1')
print(value)
