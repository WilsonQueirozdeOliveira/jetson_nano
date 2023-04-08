# Import the c_odometer class
from odometer_lib import c_odometer

# Create an instance of the c_odometer class
odometer = c_odometer()

# Update the average speed using the c_odometer instance and print it
avg_speed = odometer.update_c_odometer()
print("Average speed:", avg_speed)