--Custom profile for Anet ET4 Pro
--Created on 06/15/24
 
--Firmware: 0 = Marlin; 1 = RRF; 2 = Klipper;
firmware = 0--Additional features: 
add_checkbox_setting('auto_bed_leveling', 'Auto Bed Leveling','Use G29 Auto Leveling if the machine is equipped with one (BLTouch, Pinda, capacitive sensor, etc.)')
add_checkbox_setting(reload_bed_mesh', 'Reload the last bed-mesh','Reload the last saved bed-mesh if available)
add_checkbox_setting('use_per_path_accel', 'Uses Per-Path Acceleration', 'Manage Accelerations depending of the current path type')
add_setting('volumetric_flow', 'Volumetric Flow', 0, 20, 'Product of printing speed, layer height and nozzle diameter', 4.8)
 

 
--build_area_dimensions
bed_circular = false
--bed_radius = 155
bed_size_x_mm = 220
bed_size_y_mm = 220
bed_size_z_mm = 250
 
--extruder
extruder_count = 1
nozzle_diameter_mm_0 = 0.4
filament_diameter_mm_0 = 1.75
filament_linear_adv_factor = 0.06
 
--retraction_settings
filament_priming_mm = 0.8
priming_mm_per_sec = 25
retract_mm_per_sec = 25
 
--layer_height
z_layer_height_mm = 0.2
z_layer_height_mm_min = 0.04
z_layer_height_mm_max = 0.36
 
--printing_temperatures
extruder_temp_degree_c = 210
extruder_temp_degree_c_min = 150
extruder_temp_degree_c_max = 250
bed_temp_degree_c = 60
bed_temp_degree_c_min = 0
bed_temp_degree_c_max = 120
heated_chamber = false
--chamber_temp_degree_c = 0
--chamber_temp_degree_c_min = 0
--chamber_temp_degree_c_max = 110
 
--printing_speeds
print_speed_mm_per_sec = 80
print_speed_mm_per_sec_min = 26.67
print_speed_mm_per_sec_max = 280.0
perimeter_print_speed_mm_per_sec = 60.0
perimeter_print_speed_mm_per_sec_min = 26.67
perimeter_print_speed_mm_per_sec_max = 224.0
cover_print_speed_mm_per_sec = 60.0
cover_print_speed_mm_per_sec_min = 26.67
cover_print_speed_mm_per_sec_max = 224.0
first_layer_print_speed_mm_per_sec = 26.67
first_layer_print_speed_mm_per_sec_min = 5
first_layer_print_speed_mm_per_sec_max = 224.0
travel_speed_mm_per_sec = 240.0
travel_speed_mm_per_sec_min = 5
travel_speed_mm_per_sec_max = 500
 
--acceleration_settings
x_max_speed = 500
y_max_speed = 500
z_max_speed = 30
e_max_speed = 100
default_acc = 1000
e_prime_max_acc = 500
perimeter_acc = 500
infill_acc = 1000
x_max_acc = 1000
y_max_acc = 1000
z_max_acc = 25
e_max_acc = 1000
classic_jerk = true
default_jerk = 10
infill_jerk = 10
--default_junction_deviation = 0.04
--perimeter_junction_deviation = 0.08
--infill_junction_deviation = 0.04
--travel_junction_deviation = 0.04
 
--misc_default_settings
enable_active_temperature_control = true
add_brim = true
brim_distance_to_print_mm = 2
brim_num_contours = 3
enable_z_lift = true
z_lift_mm = 1
enable_travel_straight = false
--extruder_swap_zlift_mm = 0.2
--extruder_swap_retract_length_mm = 6.5
--extruder_swap_retract_speed_mm_per_sec = 25
 
--additional_features
use_per_path_accel = true
volumetric_flow = 6.4
auto_bed_leveling = true
reload_bed_mesh = false