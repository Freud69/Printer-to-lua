--Custom profile for Prusa MK2S
--Created on 06/14/24
 
--Firmware: 0 = Marlin; 1 = RRF; 2 = Klipper;
firmware = 0
 
--Additional features: 
add_checkbox_setting('auto_bed_leveling', 'Auto Bed Leveling','Use G29 Auto Leveling if the machine is equipped with one (BLTouch, Pinda, capacitive sensor, etc.)')
add_checkbox_setting('reload_bed_mesh', 'Reload the last bed-mesh','Reload the last saved bed-mesh if available')
add_checkbox_setting('use_per_path_accel', 'Uses Per-Path Acceleration', 'Manage Accelerations depending of the current path type')
add_setting('volumetric_flow', 'Volumetric Flow', 0, 20, 'Product of printing speed, layer height and nozzle diameter', 4.8)
 

 
--build_area_dimensions
bed_circular = false
--bed_radius = 155
bed_size_x_mm = 250
bed_size_y_mm = 210
bed_size_z_mm = 200
 
--extruder
extruder_count = 1
nozzle_diameter_mm_0 = 0.4
filament_diameter_mm_0 = 1.75
filament_linear_adv_factor = 0.03
 
--retraction_settings
filament_priming_mm = 0.8
priming_mm_per_sec = 35
retract_mm_per_sec = 35
 
--layer_height
z_layer_height_mm = 0.2
z_layer_height_mm_min = 0.04
z_layer_height_mm_max = 0.36
 
--printing_temperatures
extruder_temp_degree_c = 210
extruder_temp_degree_c_min = 150
extruder_temp_degree_c_max = 270
bed_temp_degree_c = 60
bed_temp_degree_c_min = 0
bed_temp_degree_c_max = 120
heated_chamber = false
--chamber_temp_degree_c = 0
--chamber_temp_degree_c_min = 0
--chamber_temp_degree_c_max = 110
 
--printing_speeds
print_speed_mm_per_sec = 60
print_speed_mm_per_sec_min = 5
print_speed_mm_per_sec_max = 120
perimeter_print_speed_mm_per_sec = 45.0
perimeter_print_speed_mm_per_sec_min = 5
perimeter_print_speed_mm_per_sec_max = 80
cover_print_speed_mm_per_sec = 45.0
cover_print_speed_mm_per_sec_min = 5
cover_print_speed_mm_per_sec_max = 80
first_layer_print_speed_mm_per_sec = 20.0
first_layer_print_speed_mm_per_sec_min = 5
first_layer_print_speed_mm_per_sec_max = 50
travel_speed_mm_per_sec = 180.0
travel_speed_mm_per_sec_min = 50
travel_speed_mm_per_sec_max = 500
 
--acceleration_settings
x_max_speed = 500
y_max_speed = 500
z_max_speed = 12
e_max_speed = 120
default_acc = 1000
e_prime_max_acc = 1500
perimeter_acc = 800
infill_acc = 2000
x_max_acc = 9000
y_max_acc = 9000
z_max_acc = 500
e_max_acc = 2000
classic_jerk = true
default_jerk = 10
infill_jerk = 10
--default_junction_deviation = 0.0133
--perimeter_junction_deviation = 0.0267
--infill_junction_deviation = 0.0133
--travel_junction_deviation = 0.0133
 
--misc_default_settings
enable_active_temperature_control = true
add_brim = true
brim_distance_to_print_mm = 2
brim_num_contours = 3
purge_line = true
enable_z_lift = true
z_lift_mm = 1
enable_travel_straight = false
--extruder_swap_zlift_mm = 0.2
--extruder_swap_retract_length_mm = 6.5
--extruder_swap_retract_speed_mm_per_sec = 25
 
--additional_features
use_per_path_accel = true
volumetric_flow = 4.8
auto_bed_leveling = true
reload_bed_mesh = true