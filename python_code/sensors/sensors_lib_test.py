from sensors_lib import wheel_sensor

# gpio input = 15 or 29
whell_rear_left = wheel_sensor(gpio_input=15,tire_diameter_m=0.067)

print(whell_rear_left.gpio_input)
print(whell_rear_left.tire_diameter_m)
count = 0
while count < 500:
    count += 1
    print('count: ', count)
    print('m/s: ', whell_rear_left.speed_meters_per_second())
    #print('mm/s: ', whell_rear_left.speed_meters_per_second()*1000)
