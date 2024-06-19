import numpy as np
import matplotlib.pyplot as plt
import math

class KITTmodel:
    def __init__(self):
        self.v0 = 0
        self.v = 0
        self.dt = 0.01
        self.L = 0.335
        self.z = np.array([0, 0])  # position
        self.d = np.array([0, 1])  # direction
        self.angle = 0

    def velocity(self, mode):
        self.v0 = self.v  # initial velocity
        m = 5.6  # mass of the car
        b = 10.2  # viscous drag coefficient
        Fd = b * abs(self.v0)  # determine drag
        match mode:
            case "acceleration":
                if self.v < 0:
                    F_net = 7.36 + Fd  # net force equal to max Fa + Fd
                else:
                    F_net = 7.36 - Fd  # net force equal to max Fa - Fd
            case "acceleration right":
                if self.v < 0:
                    F_net = 5.9 + Fd  # net force equal to max Fa + Fd
                else:
                    F_net = 5.9 - Fd  # net force equal to max Fa - Fd
            case "acceleration left":
                if self.v < 0:
                    F_net = 5.94 + Fd  # net force equal to max Fa + Fd
                else:
                    F_net = 5.94 - Fd  # net force equal to max Fa - Fd        
            case 'deceleration':
                if self.v < 0:
                    F_net = -8.29 + Fd  # net force equal to max Fb + Fd
                else:
                    F_net = -8.29 - Fd  # net force equal to max Fb - Fd 
            case 'left reverse':
                if self.v > 0:
                    F_net = -6.58 - Fd  # net force equal to max Fb - Fd
                else:
                    F_net = -6.58 + Fd  # net force equal to max Fb + Fd
            case 'right reverse':
                if self.v > 0:
                    F_net = -6.53 - Fd  # net force equal to max Fb - Fd
                else:
                    F_net = -6.53 + Fd  # net force equal to max Fb + Fd       
        a = F_net / m  # determine acceleration
        self.v = self.v0 + a * self.dt  # determine new velocity
            
    
    def direction(self, alpha):
        theta = ((self.v * math.sin(math.radians(alpha))) / self.L) * self.dt  # angle over which the car turns
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])  # determine the rotation vector
        self.d = np.dot(r, self.d)  # calculate the new direction vector
        
    def position(self, mode, alpha):
        self.velocity(mode)  # calculate the velocity
        self.direction(alpha)  # determine the direction
        self.z = self.z + self.v * self.dt * self.d  # determine the new position of the car
        return self.z
    

def wasd(kitt, command=None):
    pos = np.array([0,0])
    if command:
        key = command
    else:
        key = input("Enter command: ")  # using input instead of keyboard for simplicity

    if key == 'e':  # Stop for forwards
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'i':  # stop for backwards
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'a':  # left forward
        kitt.angle = -24.9
        pos = kitt.position("acceleration left", kitt.angle)
    elif key == 's':  # straight
        kitt.angle = 0
        pos = kitt.position("acceleration right", kitt.angle)
    elif key == 'd':  # right
        kitt.angle = 24.3
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'x':  # straight Backwards
        kitt.angle = 0
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'c':  # right Backwards
        kitt.angle = 24.3
        pos = kitt.position("right reverse", kitt.angle)
    elif key == 'z':  # Left Backwards
        kitt.angle = -24.9
        pos = kitt.position("left reverse", kitt.angle)
    return pos
        
        
def execute_commands(commands):
    kitt = KITTmodel()
    x_data, y_data = [], []
    for command, duration in commands:
        i = int(duration / 0.01)
        for _ in range(i):
            pos = wasd(kitt, command)
            x_data.append(pos[0])
            y_data.append(pos[1])
    return x_data, y_data

def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.xlim(0, 1.8)
    plt.ylim(-1, 1)
    plt.title('KITT Model Position - Circular Motion Test')
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
           
if __name__ == "__main__":
    # Circular motion test commands
    commands = [('a', 12)]  # Test for circular motion with continuous left turn
    x_data, y_data = execute_commands(commands)
    plot(x_data, y_data)
