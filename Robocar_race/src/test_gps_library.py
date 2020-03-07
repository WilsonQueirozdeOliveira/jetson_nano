import time
from GPS_VK2828U7G5LF import init_gps_GPRMC,read_gps,read_latitude,read_longitude,read_velocity

start = time.time()
init_gps_GPRMC()
end = time.time()
print("\n")
print("init_gps_GPRMC()")
print("time seconds", end-start)

time.sleep(3)

while True:
    start_all = time.time()
    
    print("\n")
    start = time.time()
    print(read_gps())
    end = time.time()
    print("time seconds", end-start)

    print("\n")
    start = time.time()
    print(read_latitude())
    end = time.time()
    print("time seconds", end-start)

    print("\n")
    start = time.time()
    print(read_longitude())
    end = time.time()
    print("time seconds", end-start)

    print("\n")
    start = time.time()
    print(read_velocity())
    end = time.time()
    print("time seconds", end-start)
    
    print("time seconds all", end-start_all)# tolal time cost
    time.sleep(5)