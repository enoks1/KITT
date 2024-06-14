import numpy as np
import matplotlib.pyplot as plt
import math

class KITTmodel:
    def __init__(self):
        self.v0 = 0
        self.v = 0
        self.dt = 0.1
        self.L = 0.335
        self.z = np.array([4.5, 4.5])  # position
        self.d = np.array([-1, 0])  # direction
        self.angle = 0

    def velocity(self, mode):
        self.v0 = self.v  # initial velocity
        m = 5.6  # mass of the car
        b = 10  # viscous drag coefficient
        Fd = b * abs(self.v0)  # determine drag
        if mode == 'deceleration':
            if self.v < 0:
                F_net = -7.4 + Fd  # net force equal to max Fb + Fd
            else:
                F_net = -7.4 - Fd  # net force equal to max Fb - Fd
            a = F_net / m  # determine acceleration
            self.v = self.v0 + a * self.dt  # determine new velocity
        else:
            if self.v < 0:
                F_net = 6 + Fd  # net force equal to max Fa + Fd
            else:
                F_net = 6 - Fd  # net force equal to max Fa - Fd
            a = F_net / m  # determine acceleration
            self.v = self.v0 + a * self.dt  # determine new velocity
        return self.v

    def direction(self, alpha):
        theta = ((self.v * math.sin(math.radians(alpha))) / self.L) * self.dt  # angle over which the car turns
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])  # determine the rotation vector
        self.d = np.dot(r, self.d)  # calculate the new direction vector

    def position(self, mode, alpha):
        self.velocity(mode)  # calculate the velocity
        self.direction(alpha)  # determine the direction
        print(self.z)
        self.z = self.z + self.v * self.dt * self.d  # determine the new position of the car
        return self.z
#check of target in cirle--> door 4 if statement van enes met min(xy) max(xy)
#if in circle --> determine x_delta
    def equation_circle( x, y, radius, center_x, center_y):
        distance = np.sqrt((x-center_x)**2 + (y-center_y)**2)
        return distance < radius
        
    def check_range(self, current_x, current_y, target_x, target_y, theta_direction):
        radius = 0.85
        offset_x = radius * np.cos(90-theta_direction) 
        offset_y = radius * np.sin(90-theta_direction)
        center1_x = current_x - offset_x
        center2_x = current_x + offset_x
        center1_y = current_y + offset_y
        center2_y = current_y - offset_y
        
        check_x1 = self.equation_circle(target_x, target_y, radius, center1_x, center1_y)
        check_x2 = self.equation_circle(target_x, target_y, radius, center2_x, center2_y)

        intersections = self.find_circle_line_intersections(center1_x, center1_y, radius, theta_direction, target_x, target_y)
        if check_x1:
            return center1_x, center1_y
        elif check_x2:
            return center2_x, center2_y
        else:
            return False
    def find_circle_line_intersections(h, k, r, theta, x0, y0):
        theta = math.radians(theta)
        m = math.tan(theta)
        
        # Line equation: y = mx + c
        c = y0 - m * x0
        
        # Substitute y = mx + c into the circle equation
        A = 1 + m**2
        B = 2 * (m * c - m * k - h)
        C = h**2 + k**2 + c**2 - 2 * k * c - r**2
        
        # Quadratic equation: Ax^2 + Bx + C = 0
        discriminant = B**2 - 4 * A * C
        
        if discriminant < 0:
            # No intersection
            return None
        elif discriminant == 0:
            # One intersection (tangent line)
            x1 = -B / (2 * A)
            y1 = m * x1 + c
            return [(x1, y1)]
        else:
            # Two intersections
            sqrt_discriminant = math.sqrt(discriminant)
            x1 = (-B + sqrt_discriminant) / (2 * A)
            y1 = m * x1 + c
            x2 = (-B - sqrt_discriminant) / (2 * A)
            y2 = m * x2 + c
            return [(x1, y1), (x2, y2)]

    def get_line_eq(car_x, car_y, orientation_angle):
       
        slope = math.tan(orientation_angle)
        intercept = car_y - slope * car_x
        return slope, intercept

    def get_perpendicular_line_eq(point_x, point_y, slope):
        
        perpendicular_slope = -1 / slope
        intercept = point_y - perpendicular_slope * point_x
        return perpendicular_slope, intercept

    def get_intersection(slope1, intercept1, slope2, intercept2):
       
        x = (intercept2 - intercept1) / (slope1 - slope2)
        y = slope1 * x + intercept1
        return x, y

    def calculate_projection_coordinates(self, target_x, target_y):
        car_x = self.z[0]
        car_y = self.z[1]
        
        d0x, d0y = self.d  # direction vector
        orientation_angle = math.degrees(math.atan2(d0y, d0x))  # Angle of the direction vector in degrees
 
        if self.check_range() is not False:
            center_x, center_y = self.check_range(car_x, car_y, target_x, target_y, orientation_angle)
        else:
            return False
        # Get the equation of the line representing the car's orientation
        car_slope, car_intercept = self.get_line_eq(car_x, car_y, orientation_angle)
        proj_x1, proj_y1 = self.find_circle_line_intersections(center_x, center_y, orientation_angle,target_x,target_y)[0]
        proj_x2, proj_y2 = self.find_circle_line_intersections(center_x, center_y, orientation_angle,target_x,target_y)[1]

        # Get the equation of the perpendicular line that goes through the target
        perp_slope1, perp_intercept1 = self.get_perpendicular_line_eq(proj_x1, proj_y1, car_slope)
        perp_slope2, perp_intercept2 = self.get_perpendicular_line_eq(proj_x2, proj_y2, car_slope)
        # Find the intersection point of the car's orientation line and the perpendicular line
        new_x1, new_y1 = self.get_intersection(car_slope, car_intercept, perp_slope1, perp_intercept1)
        new_x2, new_y2 = self.get_intersection(car_slope, car_intercept, perp_slope2, perp_intercept2)
        
        return [(new_x1,new_y1),(new_x2,new_y2)]
    
    def state_tracking(self, b0x, b0y):
        current_position = self.z  # position of the car
        x_data, y_data = [], []  # For plotting the path state tracking calculates
        commands = []  # gather commands for car.py
        target_position = np.array([b0x, b0y])
        
        while np.linalg.norm(current_position - target_position) > 0.1:
            d0x, d0y = self.d  # direction vector
            theta_direction = math.degrees(math.atan2(d0y, d0x))  # Angle of the direction vector in degrees
            theta_expected = math.degrees(math.atan2(b0y - current_position[1], b0x - current_position[0]))  # Expected angle
            
            angle_diff = (theta_expected - theta_direction + 360) % 360 #+360 ensures a positive outcome, %360 ensures a range between 0 and 360 degrees
            if angle_diff > 180:
                angle_diff -= 360 #make the range go from -180 to 180
            
            if np.linalg.norm(current_position - target_position) >= 1.70:
                direction = "forward" if abs(angle_diff) < 90 else "reverse"
            
            match direction:
                case "forward":
                    if angle_diff < -5:
                        # go left
                        commands.append(('a', 0.1))
                        self.angle = -24.9
                    elif angle_diff > 5:
                        # go right
                        commands.append(('d', 0.1))
                        self.angle = 24.3
                    else:
                        # go straight
                        commands.append(('s', 0.1))
                        self.angle = 0
                case "reverse":
                    if angle_diff < -5 :
                        # go left
                        commands.append(('z', 0.1))
                        self.angle = -24.9
                    elif angle_diff > 5:
                        # go right
                        commands.append(('c', 0.1))
                        self.angle = 24.3
                    else:
                        # go straight
                        commands.append(('x', 0.1))
                        self.angle = 0
            
            current_position = self.position("acceleration" if direction == "forward" else "deceleration", self.angle)
            x_data.append(current_position[0])  # Save x coordinate of the car
            y_data.append(current_position[1])  # Save y coordinate of the car
        
        return x_data, y_data, commands

def wasd(kitt, command=None):
    pos = np.array([0, 0])
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
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 's':  # straight
        kitt.angle = 0
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'd':  # right
        kitt.angle = 24.3
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'x':  # straight Backwards
        kitt.angle = 0
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'c':  # right Backwards
        kitt.angle = 24.3
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'z':  # Left Backwards
        kitt.angle = -24.9
        pos = kitt.position("deceleration", kitt.angle)
    return pos

def execute_commands(commands):
    kitt = KITTmodel()
    x_data, y_data = [], []
    for command, duration in commands:
        i = int(duration / kitt.dt)
        for _ in range(i):
            pos = wasd(kitt, command)
            x_data.append(pos[0])
            y_data.append(pos[1])
    return x_data, y_data

def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.xlim(-2.5, 5)
    plt.ylim(-2, 5)
    plt.title('KITT Model Position')
    plt.show()

if __name__ == "__main__":
    kitt = KITTmodel()
    x_data, y_data, commands = kitt.state_tracking(3.5, 4.5)
                                        
    plot(x_data, y_data)
    x_data, y_data = execute_commands(commands)
    plot(x_data, y_data)
