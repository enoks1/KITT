import serial
import keyboard
import time
import pandas as pd


class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
        self.speed = 150
        self.angle = 150
        self.carrier_frequency = (5000).to_bytes(2, byteorder='big')
        self.bit_frequency = (2500).to_bytes(2, byteorder='big')
        self.repetition_count = (1250).to_bytes(2, byteorder='big')
        self.code = 0xDEADBEEF.to_bytes(4, byteorder='big')
        self.measurements  = []
        # state variables such as speed, angle are defined here
        
    def send_command(self, command):
        self.serial.write(command.encode())
    
        
    def __del__(self):
        self.serial.close()   
             
        
    def sensor_data_distance(self):
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04')
        return data
    
    def sensor_data_voltage(self):
        self.serial.write(b'Sv\n')
        data = self.serial.read_until(b'\x04')
        return data
    
    def test_distance_with_object_placement(self):
        # KITT remains stationary
        sensor_distance = self.sensor_data_distance()
        if sensor_distance is not None:
            print(f"Measured Sensor Distance: {sensor_distance} cm")
        self.measurements.append(sensor_distance)
        print(self.measurements)
        self.serial.close()
        return self.measurements
    
    def test_bluetooth(self):
        start_time = time.time()
        self.serial.write(b'sV\n')
        data = self.serial.read_until(b'\x04')
        stop_time = time.time() - start_time
        return data, start_time, stop_time

        
if __name__ == "__main__":
    kitt = KITT('COM4')
    
    #For determining the accuracy of the sensors, their maximal range, and the field of view (beam angle)
    #To test the accuracy of the sensors make sure there are no other objects in sight, measure the distance from the left and from the right sensor to the object
    #To test the maximal range make sure there are no other objects in sight, rerun until the sensor return 0
    #To test the beam angle rerun a couple of times at different angles and note the distances from left and right
    #data = kitt.test_distance_with_object_placement()
    #print(data)
     
    # Test the Bluetooth delay 10 times
    bluetooth_delays = []
    for i in range(10):
        data, start, stop = kitt.test_bluetooth()
        bluetooth_delays.append((start, stop))
        time.sleep(1)  # Adding a small delay between tests

    # Print the start and stop times
    for i, (start, stop) in enumerate(bluetooth_delays):
        print(f"Test {i + 1}: Start Time = {start}, Stop Time = {stop}, Delay = {stop - start} seconds")
        
    #For testing the delay in python code and bluetooth
    #print("Testing the delay of the distance sensor")
    #start_time = time.time()
    #a=kitt.test_distance_with_object_placement()
    #stop_time = time.time() - start_time
    #print(stop_time)
    
    #For testing the delay in python code and bluetooth
    #print("Starting distance measurement test with object placement...")
    #measurement_data = kitt.test_bluetooth()
    #print(measurement_data)
    
    

