import threading
import random
import time

def runSensors(lock, data, sensor_procedures, **kwargs):
    for sensor_procedure in sensor_procedures:
        threading.Thread(target=sensor_procedure, args=(lock, data)).start()

def create_virtual_sensor(sleep_time, sensor_name, run_sampler):
    def run_virutal_sensor(lock, data):
        while True:
            sampled_data = run_sampler()

            temp_dic = {}
            temp_dic['data'] = sampled_data
            temp_dic['timestamp'] = time.time()

            lock.acquire()
            if sensor_name in data.keys():
                data[sensor_name].append(temp_dic)
            else:
                data[sensor_name] = [temp_dic]
            lock.release()

            time.sleep(sleep_time)
    return run_virutal_sensor

virtual_sensors = [
    create_virtual_sensor(random.uniform(1,3),
                          "temperature",
                          lambda: random.randint(7,23)),
    create_virtual_sensor(random.uniform(1,3),
                          "motion",
                          lambda: random.getrandbits(1)),
    create_virtual_sensor(random.uniform(1,3),
                          "human",
                          lambda: random.sample(["John", "Alex", "Mary", "Vasya", "Unknwon"],
                                                random.randint(0, 2))),

    create_virtual_sensor(random.uniform(1,3),
                          "lightLevel",
                          lambda: random.uniform(0.00001,100000)),
    create_virtual_sensor(random.uniform(1,3),
                          "humidity",
                          lambda: random.randint(30,80)), # %
    create_virtual_sensor(random.uniform(1,3),
                          "gasLevel",
                          lambda: random.randint(0,100)), # %

    create_virtual_sensor(random.uniform(1,3),
                          "PM2.5",
                          lambda: random.randint(0,250)), # μg/m³
    create_virtual_sensor(random.uniform(1,3),
                          "carbonDioxide",
                          lambda: random.randint(0,2000)), # ppm
    create_virtual_sensor(random.uniform(1,3),
                          "waterTemperature",
                          lambda: random.randint(0,100)) 
]


#               "doorState": random.getrandbits(1),
#               "windowState": random.getrandbits(1),
#               "windSpeed": random.uniform(0,50) # m/s

        

