import threading
import random
import time

def runSensors(lock, data, sensorType, **kwargs):
    for sensor in sensorType:
        threading.Thread(target=create_sensor_data,args=(random.uniform(1,3), lock, data, sensor)).start()
    # threading.Thread(target=sensor_motion,args=(2,)).start()
    # threading.Thread(target=sensor_human,args=(1.5,)).start()
    # threading.Thread(target=sensor_light, args=(2,)).start()

possible_humans = ["John", "Alex", "Mary", "Vasya", "Unknwon"]
def create_sensor_data(sleep, lock, data, sensor):
    while True:
        lock.acquire()
        temp_dic = {}
        randomData = {"temperature": random.randint(7,23),
                      "motion": random.getrandbits(1),
                      "human": random.sample(possible_humans, random.randint(0, 2)),
                      "lightLevel": random.uniform(0.00001,100000),
                      "humidity": random.randint(30,80), # %
                      "gasLevel": random.randint(0,100), # %
                      "PM2.5": random.randint(0,250), # μg/m³
                      "carbonDioxide": random.randint(0,2000), # ppm
                      "waterTemperature": random.randint(0,100),
                      "doorState": random.getrandbits(1),
                      "windowState": random.getrandbits(1),
                      "windSpeed": random.uniform(0,50) # m/s
                      }
        temp_dic['data'] = randomData.get(sensor)
        temp_dic['timestamp'] = time.time()
        if sensor in data.keys():
            data[sensor].append(temp_dic)
        else:
            data[sensor] = [temp_dic]
        lock.release()
        time.sleep(sleep)

# def sensor_motion(sleep):
#     while True:
#         global lock
#         lock.acquire()
        
#         global data
#         temp_dic = {}
#         motion = random.getrandbits(1)
#         temp_dic['data'] = motion
#         temp_dic['timestamp'] = time.time()
#         if 'motion' in data.keys():
#             data['motion'].append(temp_dic)
#         else:
#             data['motion'] = [temp_dic]
#         lock.release()
#         time.sleep(sleep)

# possible_humans = ["John", "Alex", "Mary", "Vasya", "Unknwon"]
# def sensor_human(sleep):
#     while True:
#         globals.lock.acquire()

#         temp_dic = {}
#         num_humans = random.randint(0, 2)
#         humans = random.sample(possible_humans, num_humans)
#         temp_dic['data'] = humans
#         temp_dic['timestamp'] = time.time()
#         if 'human' in data.keys():
#             globals.data['human'].append(temp_dic)
#         else:
#             globals.data['human'] = [temp_dic]
#         globals.lock.release()
#         time.sleep(sleep)

# def sensor_light(sleep):
#     while True:
#         global lock
#         lock.acquire()
#         global data
#         temp_dic = {}
#         light = random.uniform(0.00001,100000)
#         temp_dic['data'] = light
#         temp_dic['timestamp'] = time.time()
#         if 'lightLevel' in data.keys():
#             data['lightLevel'].append(temp_dic)
#         else:
#             data['lightLevel'] = [temp_dic]
#         lock.release()
#         time.sleep(sleep)
