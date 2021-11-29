from gpiozero import CPUTemperature

def real_temp_sensor(lock, data):
    while True:
        cpu = CPUTemperature()
        print(cpu.temperature)
    
        temp_dic = {}
        cpu = CPUTemperature()
        temp_dic['data'] = cpu.temperature
        temp_dic['timestamp'] = time.time()
        sensor_name = "cpu_temp"
        lock.acquire()
        if sensor_name in data.keys():
            data[sensor_name].append(temp_dic)
        else:
            data[sensor_name] = [temp_dic]
        lock.release()
        time.sleep(1)
