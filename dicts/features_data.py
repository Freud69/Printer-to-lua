# dictionary for basic infos on the printer
tmp_default_features = {
}

default_features = {
    "build_area_dimensions": {
        "bed_circular": False,
        "bed_radius": 155,
        "bed_size_x_mm": 310,
        "bed_size_y_mm": 310,
        "bed_size_z_mm": 340,
    },
    "extruder": {
        "extruder_count": 1,
        "nozzle_diameter_mm_0": 0.4,
        "filament_diameter_mm_0": 1.75,
        "filament_linear_adv_factor": 0.06,
    },
}

# intermediate variables used to define features rescaled from others
default_printing_speed = 60
default_jerk = 20
infill_jerk = 20
default_accel = 3000
default_layer_height = 0.2
default_nozzle_diameter = 0.4


# main dictionary with every feature needed to print, at least for most printers.
features_dict = {
    "retraction_settings": {
        "filament_priming_mm": 0.8,
        "priming_mm_per_sec": 25,
        "retract_mm_per_sec": 25,
    },
    "layer_height": {
        "z_layer_height_mm": 0.2,
        "z_layer_height_mm_min": round(
            default_features["extruder"]["nozzle_diameter_mm_0"] * 0.10, 2
        ),
        "z_layer_height_mm_max": round(
            default_features["extruder"]["nozzle_diameter_mm_0"] * 0.80, 2
        ),
    },
    "printing_temperatures": {
        "extruder_temp_degree_c": 210,
        "extruder_temp_degree_c_min": 150,
        "extruder_temp_degree_c_max": 250,
        "bed_temp_degree_c": 60,
        "bed_temp_degree_c_min": 0,
        "bed_temp_degree_c_max": 120,
        "heated_chamber": False,
        "chamber_temp_degree_c": 0,
        "chamber_temp_degree_c_min": 0,
        "chamber_temp_degree_c_max": 110,
    },
    "printing_speeds": {
        "print_speed_mm_per_sec": default_printing_speed,
        "print_speed_mm_per_sec_min": default_printing_speed / 3,
        "print_speed_mm_per_sec_max": default_printing_speed * 3.5,
        "perimeter_print_speed_mm_per_sec": default_printing_speed * 0.75,
        "perimeter_print_speed_mm_per_sec_min": default_printing_speed / 3,
        "perimeter_print_speed_mm_per_sec_max": default_printing_speed * 2.8,
        "cover_print_speed_mm_per_sec": default_printing_speed * 0.75,
        "cover_print_speed_mm_per_sec_min": default_printing_speed / 3,
        "cover_print_speed_mm_per_sec_max": default_printing_speed * 2.8,
        "first_layer_print_speed_mm_per_sec": default_printing_speed / 3,
        "first_layer_print_speed_mm_per_sec_min": 5,
        "first_layer_print_speed_mm_per_sec_max": default_printing_speed * 2.8,
        "travel_speed_mm_per_sec": default_printing_speed * 3,
        "travel_speed_mm_per_sec_min": 50,
        "travel_speed_mm_per_sec_max": 500,
    },
    "acceleration_settings": {
        "x_max_speed": 500,
        "y_max_speed": 500,
        "z_max_speed": 30,
        "e_max_speed": 100,
        "default_acc": default_accel,
        "e_prime_max_acc": default_accel / 2,
        "perimeter_acc": default_accel / 2,
        "infill_acc": default_accel,
        "x_max_acc": default_accel,
        "y_max_acc": default_accel,
        "z_max_acc": default_accel / 40,
        "e_max_acc": default_accel,
        "classic_jerk": False,
        "default_jerk": default_jerk,
        "infill_jerk": default_jerk,
        "default_junction_deviation": round(0.4 * (default_jerk**2 / default_accel), 4),
        "perimeter_junction_deviation": round(
            0.4 * (default_jerk**2 / default_accel), 4
        ),
        "infill_junction_deviation": round(0.4 * (infill_jerk**2 / default_accel), 4),
        "travel_junction_deviation": round(0.4 * (default_jerk**2 / default_accel), 4),
    },
    "misc_default_settings": {
        "enable_active_temperature_control": True,
        "add_brim": True,
        "brim_distance_to_print_mm": 2,
        "brim_num_contours": 3,
        "enable_z_lift": True,
        "z_lift_mm": 1,
        "enable_travel_straight": True,
        "extruder_swap_zlift_mm": 0.2,
        "extruder_swap_retract_length_mm": 6.5,
        "extruder_swap_retract_speed_mm_per_sec": 25,
    },
    "additional_features": {
        "use_per_path_accel": False,
        "volumetric_flow": round(default_printing_speed*default_layer_height*default_nozzle_diameter, 2),
        "auto_bed_leveling": False,
        "reload_bed_mesh": False,
    },
}

#features for the Profiles folder
quality_features = {
    "layer_thickness_changes": {"z_layer_height_mm": 0.2},
    "speed_changes": {
        "print_speed_mm_per_sec": 60,
        "perimeter_print_speed_mm_per_sec": 30,
        "cover_print_speed_mm_per_sec": 30,
        "first_layer_print_speed_mm_per_sec": 20,
        "travel_speed_mm_per_sec": 80,
        "priming_mm_per_sec": 40,
        "retract_mm_per_sec": 40,
        "speed_multiplier_0": 1,
    },
}

#features for the Materials folder
materials_features = {
    "retraction_changes": {
        "filament_priming_mm": 0.8,
    },
    "temperature_changes": {
        "extruder_temp_degree_c": 210,
        "bed_temp_degree_c": 60,
        "chamber_temp_degree_c": 0,
        "enable_fan": True,
        "fan_speed_percent": 100,
        "fan_speed_percent_on_bridges": 100,
    },
    "speed_changes": {
        "print_speed_mm_per_sec": 60,
        "perimeter_print_speed_mm_per_sec": 45,
        "cover_print_speed_mm_per_sec": 30,
        "first_layer_print_speed_mm_per_sec": 20,
    },
}

# list of advanced features that are mostly rescaled values of defining features, hidden by default.
# Used in main.py to enable/disable their display.
advanced_features = [
    "enable_active_temperature_control",
    "filament_linear_adv_factor",
    "perimeter_print_speed_mm_per_sec",
    "cover_print_speed_mm_per_sec",
    "first_layer_print_speed_mm_per_sec",
    "travel_speed_mm_per_sec",
    "enable_travel_straight",
]
advanced_features += [feature for feature in features_dict["retraction_settings"]]
advanced_features += [
    feature
    for category in features_dict
    for feature in features_dict[category]
    if (
        feature.endswith("min")
        or feature.endswith("max")
        or feature.startswith("extruder_swap")
    )
]
advanced_features += [feature for feature in features_dict["additional_features"]]

#list of features disabled on startup. They may be so because they depend on another feature
start_as_disabled = [
    "default_jerk",
    "infill_jerk",
    "chamber_temp_degree_c",
    "chamber_temp_degree_c_min",
    "chamber_temp_degree_c_max",
    "reload_bed_mesh"
]
# list of acceleration features. Hidden by default and only accessible when acceleration is enabled in advanced mode.
accel_features = [feature for feature in features_dict["acceleration_settings"]]
