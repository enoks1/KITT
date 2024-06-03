import serial
import time
import matplotlib.pyplot as plt #install with: pip install matplotlib
class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
        self.speed = 150
        self.angle = 150
        self.carrier_frequency = (5000).to_bytes(2, byteorder='big')
        self.bit_frequency = (2500).to_bytes(2, byteorder='big')
        self.repetition_count = (1250).to_bytes(2, byteorder='big')
        self.code = 0xDEADBEEF.to_bytes(4, byteorder='big')
        self.measurements = []
        # state variables such as speed, angle are defined here
    def send_command(self, command):
        self.serial.write(command.encode())
    
    def set_speed(self, speed):
        self.speed = speed #set speed
        self.send_command(f'M{speed}\n')
    
    def set_angle(self, angle):
        self.angle = angle #set angle
        self.send_command(f'D{angle}\n')

    def stop(self):
        self.set_speed(150)
        self.set_angle(150)
        self.send_command('R')
        
    def emergency_brake(self):
        current_speed=self.speed
        if(current_speed>150):
            self.set_speed(135)
            time.sleep(0.5)  # Brake for 1 second
            self.set_speed(150)   
        elif(current_speed<150):
            self.set_speed(165)
            time.sleep(0.3)  # Brake for 1 second
            self.set_speed(150) 
        else: 
            self.set_speed(150) 
        
    def sensor_data(self):
        self.serial.write(b'Sv\n')
        vdata = self.serial.read_until(b'\x04').decode()
        voltage =  vdata.split('VBATT')[1][:4]
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04').decode()
        left_distance = int(data.split('USL')[1][:3])  #Seperate the disctance sensors fir the left sensor. Assumes format USL###\n
        right_distance = int(data.split('USR')[1][:3])  #Seperate the disctance sensors fir the right sensor. Assumes format USR###\n
        return left_distance, right_distance, voltage
    
    def __del__(self):
        self.serial.close()
            
    def run_distance_measurement(self):
        current_time = time.time()
        t_end = current_time + 5
        
        try:
            while time.time() < t_end:
                # Move sensor data collection inside the loop to update readings continuously
                left_distance, right_distance, voltage = self.sensor_data()
                current_time = time.time()  # Update current time inside the loop
                self.set_speed(160)  # Assuming you want to maintain this speed during the measurement period
                self.measurements.append((current_time, left_distance, right_distance, voltage))  # Log the time and distance
        finally:
                self.emergency_brake()
                self.__del__()  # Break connection with KITT
        return self.measurements  # Return the collected measurements
     
def plot_distance_vs_time(measurements):
    times = [m[0] for m in measurements]
    left_distances = [m[1] for m in measurements]
    right_distances = [m[2] for m in measurements]
    voltage = [float(m[3]) for m in measurements]

    # Initialize velocity with zeros
    velocity = [0] * len(times)
    for i in range(8, len(times)):
        try:
            velocity[i] = (left_distances[i-8]- left_distances[i]) / (times[i] - times[i-8])
        except ZeroDivisionError:
            velocity[i] = 0
    # Normalize time data to start from zero
    start_time = times[0]
    times = [t - start_time for t in times]

    
    plt.figure(figsize=(10, 10))
    plt.subplot(4, 2, 1)
    plt.plot(times, left_distances, marker='o', linestyle='-', color='blue', label='Left Sensor')
    plt.title('Time vs. Distance Measurement of KITT')
    plt.ylabel('Distance (cm)')
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 2, 2)
    plt.plot(times, right_distances, marker='o', linestyle='-', color='red', label='Right Sensor')
    plt.title('Time vs. Distance Measurement of KITT')
    plt.ylabel('Distance (cm)')
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 2, 3)
    plt.plot(times, voltage, marker='o', linestyle='-', color='green', label='Voltage')
    plt.title('Voltage vs. Time Measurement of KITT')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.ylim(0, 20)  # Set y-axis to range from 0 to 20 volts
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 2, 4)
    plt.plot(times, velocity, marker='o', linestyle='-', color='green', label='Velocity')
    plt.title('Velocity vs. Time Measurement of KITT')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (cm/s)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    kitt = KITT('COM3')
    #To test KITT for the overal delay in determining how far an object is, when it needs to stop and actually stopping
    #data = kitt.run_distance_measurement()
    #Plots the distance measurements vs the time. The velocity and cycle can be extracted.
    #plot_distance_vs_time(kitt.measurements)
    #kitt = KITT('COM3')
    #kitt.serial.write(b'Sv\n')
    #data = kitt.sensor_data()
    kitt.serial.close()
    #print(data) 