import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Data from the table
wheel_settings_group1 = np.array([200, 190, 180])
steering_angles_group1 = np.array([24.9, 21.5, 16.0])

wheel_settings_group2 = np.array([100, 110, 120])
steering_angles_group2 = np.array([24.3, 20.6, 15.2])

# Plotting the first group
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.scatter(wheel_settings_group1, steering_angles_group1, color='blue', label='Measured Data')
plt.xlabel('Wheel Settings (D)')
plt.ylabel('Steering Angle (degrees)')
plt.title('Turn right: Wheel Settings vs Steering Angle')
plt.grid(True)

# Fit a linear model for group 1
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(wheel_settings_group1, steering_angles_group1)

# Plot the linear fit for group 1
plt.plot(wheel_settings_group1, intercept1 + slope1 * wheel_settings_group1, 'r', label=f'Linear fit: y={intercept1:.2f}+{slope1:.2f}x\n$R^2={r_value1**2:.2f}$')
plt.legend()

# Plotting the second group
plt.subplot(1, 2, 2)
plt.scatter(wheel_settings_group2, steering_angles_group2, color='blue', label='Measured Data')
plt.xlabel('Wheel Settings (D)')
plt.ylabel('Steering Angle (degrees)')
plt.title('Turn left: Wheel Settings vs Steering Angle')
plt.grid(True)
plt.gca().invert_xaxis()  # Reverse the x-axis for Group 2

# Fit a linear model for group 2
slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(wheel_settings_group2, steering_angles_group2)

# Plot the linear fit for group 2
plt.plot(wheel_settings_group2, intercept2 + slope2 * wheel_settings_group2, 'r', label=f'Linear fit: y={intercept2:.2f}+{slope2:.2f}x\n$R^2={r_value2**2:.2f}$')
plt.legend()

plt.tight_layout()
plt.show()

# Print the linear models and R-squared values
print(f"Group 1 Linear model: Steering Angle = {intercept1:.2f} + {slope1:.2f} * Wheel Settings")
print(f"Group 1 R-squared value: {r_value1**2:.2f}")
print(f"Group 2 Linear model: Steering Angle = {intercept2:.2f} + {slope2:.2f} * Wheel Settings")
print(f"Group 2 R-squared value: {r_value2**2:.2f}")
