import threading
import random
import time

def runSensors(lock, data, **kwargs):
    threading.Thread(target=sensor_temp,args=(1, lock, data)).start()
    # threading.Thread(target=sensor_motion,args=(2,)).start()
    # threading.Thread(target=sensor_human,args=(1.5,)).start()
    # threading.Thread(target=sensor_light, args=(2,)).start()

def sensor_temp(sleep, lock, data):
    while True:
        lock.acquire()
        temp_dic = {}
        temp = random.randint(7,23)
        temp_dic['data'] = temp
        temp_dic['timestamp'] = time.time()
        if 'temperature' in data.keys():
            data['temperature'].append(temp_dic)
        else:
            data['temperature'] = [temp_dic]
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
