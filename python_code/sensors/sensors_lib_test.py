from pico_rpm_reader import PicoRPMReader
import time

def main():
    # Initialize the PicoRPMReader with the appropriate serial port
    rpm_reader = PicoRPMReader(serial_port='/dev/ttyACM0')
    rpm_reader.connect()

    try:
        while True:
            # Get the tire speed in meters per second
            tire_speed = rpm_reader.get_tire_speed()
            if tire_speed is not None:
                print(f"Tire Speed: {tire_speed:.2f} m/s")
            #time.sleep(0.1)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("\nStopped measuring tire speed.")

if __name__ == "__main__":
    main()

