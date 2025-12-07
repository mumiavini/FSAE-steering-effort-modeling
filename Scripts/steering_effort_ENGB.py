import math

# --- 1. INPUT PARAMETERS ---
# Vehicle and Suspension Parameters (your previous values)
total_vehicle_mass = 376  # kg
front_weight_distribution = 0.5
caster_angle = 4.0  # degrees
dynamic_wheel_radius = 0.23 # meters
kpi_angle = 10.0 # degrees
scrub_radius = 0.035 # meters

# Steering System Parameters (your previous values)
pinion_radius = 0.04 # meters
steering_arm_length = 0.170 # meters

# Parameters for Inertia Calculation
pinion_mass = 0.851 # Kg
pinion_moment_of_inertia = 0.000629 # Resistance to rotation in Z, from pinion CAD
rack_mass = 0.587 # Kg

# for static friction
tire_pressure = 0.83 # bar (ex: 12 PSI)
pneumatic_trail = 0.025

# Analysis Scenario Parameters
lateral_acceleration = 0 * 9.81 # m/s^2. IMPORTANT: Keep at 0 for stationary car analysis.
estimated_system_friction = 4 # Nm (internal mechanical friction of the steering system)
average_wheel_steer_angle = 38.77 # degrees (angle for which the effort will be calculated)


# --- 2. CALCULATIONS ---
rack_moment_of_inertia = rack_mass * pinion_radius**2 # Concentrated mass at distance "d" from the center of rotation
effective_moment_of_inertia = rack_moment_of_inertia + pinion_moment_of_inertia
front_axle_mass = total_vehicle_mass * front_weight_distribution
vertical_load_per_wheel = (front_axle_mass * 9.81) / 2
caster_rad = math.radians(caster_angle)
kpi_rad = math.radians(kpi_angle)
steer_angle_rad = math.radians(average_wheel_steer_angle)
mechanical_trail = dynamic_wheel_radius * math.tan(caster_rad)
total_steering_ratio_i_S = (1 / pinion_radius) * steering_arm_length

# --- SEPARATE CALCULATION LOGIC FOR STATIONARY AND MOVING CAR ---

if lateral_acceleration == 0:
    # --- SCENARIO: STATIONARY CAR ---
    
    # 1. Calculate Scrub Torque (Resistive)
    static_friction_coeff_tire_ground = 1.4 # Dimensionless (value for rubber on dry asphalt, static)
    tire_pressure_pascal = tire_pressure * 100000
    estimated_contact_patch_area = vertical_load_per_wheel / tire_pressure_pascal # m^2
    estimated_patch_radius = math.sqrt(estimated_contact_patch_area / math.pi) # m
    
    scrub_torque_per_wheel = (2/3) * static_friction_coeff_tire_ground * vertical_load_per_wheel * estimated_patch_radius # Nm

    # 2. Calculate Jacking Moment (Restoring/Opposes the pilot)
    jacking_moment_per_wheel = vertical_load_per_wheel * (scrub_radius * math.tan(kpi_rad) + mechanical_trail * math.tan(caster_rad)) * math.sin(steer_angle_rad)
    
    # 3. Resultant moment on the kingpin that the pilot must overcome
    total_kingpin_moment_per_wheel = scrub_torque_per_wheel + jacking_moment_per_wheel

    # 4. Calculation of Steering Wheel Effort
    steering_wheel_effort_no_friction = (total_kingpin_moment_per_wheel * 2) / total_steering_ratio_i_S
    total_steering_wheel_effort = steering_wheel_effort_no_friction + estimated_system_friction

else:
    # --- SCENARIO: MOVING CAR ---
    total_front_lateral_force = front_axle_mass * lateral_acceleration
    lateral_force_per_wheel = total_front_lateral_force / 2
    total_ground_trail = mechanical_trail + pneumatic_trail
    
    # 1. Calculate Self-Aligning Torque (Resistive)
    self_aligning_torque = lateral_force_per_wheel * total_ground_trail

    # 2. Calculate Jacking Moment (Restoring/Opposes the pilot)
    jacking_moment_per_wheel = vertical_load_per_wheel * (scrub_radius * math.tan(caster_rad) + mechanical_trail * math.tan(kpi_rad)) * math.sin(steer_angle_rad)

    # 3. Resultant moment on the kingpin that the pilot must overcome
    total_kingpin_moment_per_wheel = self_aligning_torque + jacking_moment_per_wheel

    # 4. Calculation of Steering Wheel Effort
    steering_wheel_effort_no_friction = (total_kingpin_moment_per_wheel * 2) / total_steering_ratio_i_S
    total_steering_wheel_effort = steering_wheel_effort_no_friction + estimated_system_friction


# --- 3. RESULTS ---
print(f"--- STEERING EFFORT ANALYSIS (Scenario: Stationary Car) ---")
print(f"Analyzed Steer Angle: {average_wheel_steer_angle:.1f}°")
print("-" * 70)
if lateral_acceleration == 0:
    print(f"Decomposition of Moments (per wheel):")
    print(f"  - Moment of Inertia (Resistive): {effective_moment_of_inertia:.4f} kg x m²")
    print(f"  - Scrub Torque (Resistive): {scrub_torque_per_wheel:.2f} Nm")
    print(f"  - Jacking Moment (Restoring): {jacking_moment_per_wheel:.2f} Nm")
    print(f"  - RESULTANT MOMENT to be overcome at the kingpin: {total_kingpin_moment_per_wheel:.2f} Nm")
    print("-" * 70)
    print(f"Final Result (Stationary Car):")
    print(f"  - Steering Wheel Effort (without internal friction): {steering_wheel_effort_no_friction:.2f} Nm")
    print(f"  - Total Steering Wheel Effort (with internal friction): {total_steering_wheel_effort:.2f} Nm")
else:
    # (Output for moving car, as before)
    print(f"Decomposition of Moments (per wheel):")
    print(f"  - Moment of Inertia (Resistive): {effective_moment_of_inertia:.2f} kg x m²")
    print(f"  - Self-Aligning Torque (Restoring): {self_aligning_torque:.2f} Nm")
    print(f"  - Jacking Moment (Restoring): {jacking_moment_per_wheel:.2f} Nm")
    print(f"  - RESULTANT MOMENT to be overcome at the kingpin: {total_kingpin_moment_per_wheel:.2f} Nm")
    print("-" * 70)
    print(f"Final Result (Moving Car):")
    print(f"  - Steering Wheel Effort (without internal friction): {steering_wheel_effort_no_friction:.2f} Nm")
    print(f"  - Total Steering Wheel Effort (with internal friction): {total_steering_wheel_effort:.2f} Nm")

print("-" * 70)