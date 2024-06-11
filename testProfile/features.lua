--Custom profile for testProfile
--Created on 06/08/24
 
--Firmware: 0 = Marlin; 1 = RRF; 2 = Klipper; 3 = Others
firmware = 1
 
--build_area_dimensions
bed_circular = false
--bed_radius = 155
bed_size_x_mm = 310.0
bed_size_y_mm = 310.0
bed_size_z_mm = 350
 
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
print_speed_mm_per_sec = 60
print_speed_mm_per_sec_min = 20.0
print_speed_mm_per_sec_max = 210.0
perimeter_print_speed_mm_per_sec = 45.0
perimeter_print_speed_mm_per_sec_min = 20.0
perimeter_print_speed_mm_per_sec_max = 168.0
cover_print_speed_mm_per_sec = 45.0
cover_print_speed_mm_per_sec_min = 20.0
cover_print_speed_mm_per_sec_max = 168.0
first_layer_print_speed_mm_per_sec = 20.0
first_layer_print_speed_mm_per_sec_min = 5
first_layer_print_speed_mm_per_sec_max = 168.0
travel_speed_mm_per_sec = 180.0
travel_speed_mm_per_sec_min = 50
travel_speed_mm_per_sec_max = 500
 
--acceleration_settings
x_max_speed = 500
y_max_speed = 500
z_max_speed = 30
e_max_speed = 100
default_acc = 3000
e_prime_max_acc = 1500
perimeter_acc = 1500
infill_acc = 3000
x_max_acc = 3000
y_max_acc = 3000
z_max_acc = 75
e_max_acc = 3000
--classic_jerk = false
--default_jerk = 20
--infill_jerk = 20
default_junction_deviation = 0.0533
perimeter_junction_deviation = 0.1067
infill_junction_deviation = 0.0533
travel_junction_deviation = 0.0533
 
--misc_default_settings
enable_active_temperature_control = true
add_brim = true
brim_distance_to_print_mm = 2
brim_num_contours = 3
enable_z_lift = true
z_lift_mm = 1
enable_travel_straight = true
--extruder_swap_zlift_mm = 0.2
--extruder_swap_retract_length_mm = 6.5
--extruder_swap_retract_speed_mm_per_sec = 25
 
--additional_features
use_per_path_accel = false
volumetric_flow = 4.8
auto_bed_leveling = false
--reload_bed_mesh = false