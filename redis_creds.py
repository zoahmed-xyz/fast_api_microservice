import redis

HOST = 'redis-17255.c1.us-central1-2.gce.cloud.redislabs.com'
PORT = 17255
PASSWORD = 'Cr6n6ec8P7GiKPV0Y2FF9EFixcLtM9Sd'

if __name__ == "__main__":
  r = redis.Redis(
    host= HOST,
    port= PORT,
    password= PASSWORD)