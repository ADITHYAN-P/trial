import serial
import time

# Initialize UART for SIM808 communication
sim808 = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

def check_gsm_status():
    """
    Check if the GSM module is active and connected to the network.
    """
    sim808.write(b'AT+CREG?\r')
    time.sleep(1)
    response = sim808.readlines()
    for line in response:
        print(line.decode().strip())
        if "+CREG: 0,1" in line.decode() or "+CREG: 0,5" in line.decode():
            print("GSM is active and registered on the network.")
            return True
    print("GSM is not registered or inactive.")
    return False

def get_gps_data():
    """
    Retrieve GPS data: latitude, longitude, and speed.
    """
    # Turn on GPS
    sim808.write(b'AT+CGNSPWR=1\r')
    time.sleep(2)

    # Request GPS information
    sim808.write(b'AT+CGNSINF\r')
    time.sleep(2)

    response = sim808.readlines()
    for line in response:
        if b'+CGNSINF' in line:
            gps_data = line.decode().split(',')
            latitude = gps_data[3]
            longitude = gps_data[4]
            speed = gps_data[6]
            
            if latitude and longitude:
                print(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed} km/h")
            else:
                print("GPS data unavailable.")
            break
    else:
        print("Failed to retrieve GPS data.")

# Main function
def main():
    try:
        if check_gsm_status():
            print("Fetching GPS data...")
            get_gps_data()
        else:
            print("Please check GSM module and network coverage.")
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        # Turn off GPS to save power
        sim808.write(b'AT+CGNSPWR=0\r')
        print("GPS powered off.")

if _name_ == "_main_":
    main()
