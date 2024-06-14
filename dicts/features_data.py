# dictionary for basic infos on the printer

###intermediate variables used to define features rescaled from others
default_printing_speed = 60
default_jerk = 10
infill_jerk = 10
default_accel = 3000
default_layer_height = 0.2
default_nozzle_diameter = 0.4

###Temp dict revamped to be more readable and easier to maintain
#each tuples follows the format (default_value, type, min_value, max_value, isHidden, isDisabled)
default_features = {
    "build_area_dimensions": {
        "bed_circular": (False, "bool", None, None, False, False),
        "bed_radius": (155, "int", 50, 200, True, False),
        "bed_size_x_mm": (310, "int", 50, None, False, False),
        "bed_size_y_mm": (310, "int", 50, None, False, False),
        "bed_size_z_mm": (340, "int", 50, None, False, False),
    },
    "extruder": {
        "extruder_count": (1, "int", 1, 14, False, False),
        "nozzle_diameter_mm_0": (0.4, "float", 0.25, 0.6, False, False),
        "filament_diameter_mm_0": (1.75, "float", 1.25, 2.25, False, False),
        "filament_linear_adv_factor": (0.06, "float", 0.0, 0.2, True, False),
    },
}

features_dict = {
    "retraction_settings": {
        "filament_priming_mm": (0.8, "float", 0, 100, True, False),
        "priming_mm_per_sec": (25, "int", 0, 100, True, False),
        "retract_mm_per_sec": (25, "int", 0, 100, True, False),
    },
    "layer_height": {
        "z_layer_height_mm": (0.2, "float", 0, 100, False, False),
        "z_layer_height_mm_min": (
            round(default_features["extruder"]["nozzle_diameter_mm_0"][0] * 0.10, 2),
            "float",
            0,
            100,
            True,
            False,
        ),
        "z_layer_height_mm_max": (
            round(default_features["extruder"]["nozzle_diameter_mm_0"][0] * 0.80, 2),
            "float",
            0,
            100,
            True,
            False,
        ),
    },
    
        "printing_temperatures": {
        "extruder_temp_degree_c": (210, "int", 0, 300, False, False),
        "extruder_temp_degree_c_min": (150, "int", 0, 300, True, False),
        "extruder_temp_degree_c_max": (250, "int", 0, 300, True, False),
        "bed_temp_degree_c": (60, "int", 0, 100, False, False),
        "bed_temp_degree_c_min": (0, "int", 0, 100, True, False),
        "bed_temp_degree_c_max": (120, "int", 60, 130, True, False),
        "heated_chamber": (False, "bool", None, None, False, False),
        "chamber_temp_degree_c": (0, "int", 0, 100, False, True),
        "chamber_temp_degree_c_min": (0, "int", 0, 100, True, True),
        "chamber_temp_degree_c_max": (110, "int", 0, 130, True, True),
    },
    "printing_speeds": {
        "print_speed_mm_per_sec": (default_printing_speed, "int", 0, 100, False, False),
        "print_speed_mm_per_sec_min": (default_printing_speed / 3, "float", 0, 100, True, False),
        "print_speed_mm_per_sec_max": (default_printing_speed * 3.5, "float", 0, 300, True, False),
        "perimeter_print_speed_mm_per_sec": (default_printing_speed * 0.75, "float", 0, 100, False, False),
        "perimeter_print_speed_mm_per_sec_min": (default_printing_speed / 3, "float", 0, 100, True, False),
        "perimeter_print_speed_mm_per_sec_max": (default_printing_speed * 2.8, "float", 0, 300, True, False),
        "cover_print_speed_mm_per_sec": (default_printing_speed * 0.75, "float", 0, 100, False, False),
        "cover_print_speed_mm_per_sec_min": (default_printing_speed / 3, "float", 0, 100, True, False),
        "cover_print_speed_mm_per_sec_max": (default_printing_speed * 2.8, "float", 0, 300, True, False),
        "first_layer_print_speed_mm_per_sec": (default_printing_speed / 3, "float", 0, 100, False, False),
        "first_layer_print_speed_mm_per_sec_min": (5, "int", 0, 100, True, False),
        "first_layer_print_speed_mm_per_sec_max": (default_printing_speed * 2.8, "float", 0, 300, True, False),
        "travel_speed_mm_per_sec": (default_printing_speed * 3, "float", 0, 500, False, False),
        "travel_speed_mm_per_sec_min": (50, "int", 0, 100, True, False),
        "travel_speed_mm_per_sec_max": (500, "int", 0, 750, True, False),

    },"acceleration_settings": {
        "x_max_speed": (500, "int", 0, 10000, True, True),
        "y_max_speed": (500, "int", 0, 10000, True, True),
        "z_max_speed": (30, "int", 0, 10000, True, True),
        "e_max_speed": (100, "int", 0, 1000, True, True),
        "default_acc": (default_accel, "int", 0, 1000, True, True),
        "e_prime_max_acc": (default_accel / 2, "float", 0, 1000, True, True),
        "perimeter_acc": (default_accel / 2, "float", 0, 1000, True, True),
        "infill_acc": (default_accel, "int", 0, 1000, True, True),
        "x_max_acc": (default_accel, "int", 0, 1000, True, True),
        "y_max_acc": (default_accel, "int", 0, 1000, True, True),
        "z_max_acc": (default_accel / 40, "float", 0, 1000, True, True),
        "e_max_acc": (default_accel, "int", 0, 1000, True, True),
        "classic_jerk": (False, "bool", None, None, True, True),
        "default_jerk": (default_jerk, "int", 0, 1000, True, True),
        "infill_jerk": (infill_jerk, "int", 0, 1000, True, True),
        "default_junction_deviation": (round(0.4 * (default_jerk**2 / default_accel), 4), "float", 0, 1000, True, True),
        "perimeter_junction_deviation": (round(0.4 * (default_jerk**2 / default_accel / 2), 4), "float", 0, 1000, True, True),
        "infill_junction_deviation": (round(0.4 * (infill_jerk**2 / default_accel), 4), "float", 0, 1000, True, True),
        "travel_junction_deviation": (round(0.4 * (default_jerk**2 / default_accel), 4), "float", 0, 1000, True, True),
    },
    "misc_default_settings": {
        "enable_active_temperature_control": (True, "bool", None, None, True, False),
        "add_brim": (True, "bool", None, None, False, False),
        "brim_distance_to_print_mm": (2, "int", 0, 100, False, False),
        "brim_num_contours": (3, "int", 0, 100, False, False),
        "purge_line": (True, "bool", None, None, False, False),
        "enable_z_lift": (True, "bool", None, None, False, False),
        "z_lift_mm": (1, "int", 0, 100, False, False),
        "enable_travel_straight": (True, "bool", None, None, True, False),
        "extruder_swap_zlift_mm": (0.2, "float", 0, 100, True, False),
        "extruder_swap_retract_length_mm": (6.5, "float", 0, 100, True, False),
        "extruder_swap_retract_speed_mm_per_sec": (25, "int", 0, 100, True, False),
    },
    "additional_features": {
        "use_per_path_accel": (True, "bool", None, None, True, False),
        "volumetric_flow": (round(default_printing_speed*default_layer_height*default_nozzle_diameter, 2), "float", 0, 100, True, False),
        "auto_bed_leveling": (True, "bool", None, None, True, False),
        "reload_bed_mesh": (False, "bool", None, None, True, True),
    },
}

quality_features = {
    "layer_thickness_changes": {
        "z_layer_height_mm": (0.2, "float", 0, 100, False, False)
    },
    "speed_changes": {
        "print_speed_mm_per_sec": (60, "int", 0, 100, False, False),
        "perimeter_print_speed_mm_per_sec": (30, "int", 0, 100, False, False),
        "cover_print_speed_mm_per_sec": (30, "int", 0, 100, False, False),
        "first_layer_print_speed_mm_per_sec": (20, "int", 0, 100, False, False),
        "travel_speed_mm_per_sec": (80, "int", 0, 100, False, False),
        "priming_mm_per_sec": (40, "int", 0, 100, False, False),
        "retract_mm_per_sec": (40, "int", 0, 100, False, False),
        "speed_multiplier_0": (1, "int", 0, 100, False, False),
    },
}

materials_features = {
    "extruder": {
        "filament_linear_adv_factor": (0.06, "float", 0, 0.2, False, False),
    },
    "retraction_changes": {
        "filament_priming_mm": (0.8, "float", 0, 100, False, False),
    },
    "temperature_changes": {
        "extruder_temp_degree_c": (210, "int", 0, 280, False, False),
        "bed_temp_degree_c": (60, "int", 0, 100, False, False),
        "chamber_temp_degree_c": (0, "int", 0, 100, False, False),
        "enable_fan": (True, "bool", None, None, False, False),
        "fan_speed_percent": (100, "int", 0, 100, False, False),
        "fan_speed_percent_on_bridges": (100, "int", 0, 100, False, False),
    },
    "speed_changes": {
        "print_speed_mm_per_sec": (60, "int", 0, 100, False, False),
        "perimeter_print_speed_mm_per_sec": (45, "int", 0, 100, False, False),
        "cover_print_speed_mm_per_sec": (30, "int", 0, 100, False, False),
        "first_layer_print_speed_mm_per_sec": (20, "int", 0, 100, False, False),
    },
}

### OLD dicts
# main dictionary with every feature needed to print, at least for most printers.
# default_features = {
#     "build_area_dimensions": {
#         "bed_circular": False,
#         "bed_radius": 155,
#         "bed_size_x_mm": 310,
#         "bed_size_y_mm": 310,
#         "bed_size_z_mm": 340,
#     },
#     "extruder": {
#         "extruder_count": 1,
#         "nozzle_diameter_mm_0": 0.4,
#         "filament_diameter_mm_0": 1.75,
#         "filament_linear_adv_factor": 0.06,
#     },
# }
# features_dict = {
#     "retraction_settings": {
#         "filament_priming_mm": 0.8,
#         "priming_mm_per_sec": 25,
#         "retract_mm_per_sec": 25,
#     },
#     "layer_height": {
#         "z_layer_height_mm": 0.2,
#         "z_layer_height_mm_min": round(
#             default_features["extruder"]["nozzle_diameter_mm_0"] * 0.10, 2
#         ),
#         "z_layer_height_mm_max": round(
#             default_features["extruder"]["nozzle_diameter_mm_0"] * 0.80, 2
#         ),
#     },
#     "printing_temperatures": {
#         "extruder_temp_degree_c": 210,
#         "extruder_temp_degree_c_min": 150,
#         "extruder_temp_degree_c_max": 250,
#         "bed_temp_degree_c": 60,
#         "bed_temp_degree_c_min": 0,
#         "bed_temp_degree_c_max": 120,
#         "heated_chamber": False,
#         "chamber_temp_degree_c": 0,
#         "chamber_temp_degree_c_min": 0,
#         "chamber_temp_degree_c_max": 110,
#     },
#     "printing_speeds": {
#         "print_speed_mm_per_sec": default_printing_speed,
#         "print_speed_mm_per_sec_min": default_printing_speed / 3,
#         "print_speed_mm_per_sec_max": default_printing_speed * 3.5,
#         "perimeter_print_speed_mm_per_sec": default_printing_speed * 0.75,
#         "perimeter_print_speed_mm_per_sec_min": default_printing_speed / 3,
#         "perimeter_print_speed_mm_per_sec_max": default_printing_speed * 2.8,
#         "cover_print_speed_mm_per_sec": default_printing_speed * 0.75,
#         "cover_print_speed_mm_per_sec_min": default_printing_speed / 3,
#         "cover_print_speed_mm_per_sec_max": default_printing_speed * 2.8,
#         "first_layer_print_speed_mm_per_sec": default_printing_speed / 3,
#         "first_layer_print_speed_mm_per_sec_min": 5,
#         "first_layer_print_speed_mm_per_sec_max": default_printing_speed * 2.8,
#         "travel_speed_mm_per_sec": default_printing_speed * 3,
#         "travel_speed_mm_per_sec_min": 50,
#         "travel_speed_mm_per_sec_max": 500,
#     },
#     "acceleration_settings": {
#         "x_max_speed": 500,
#         "y_max_speed": 500,
#         "z_max_speed": 30,
#         "e_max_speed": 100,
#         "default_acc": default_accel,
#         "e_prime_max_acc": default_accel / 2,
#         "perimeter_acc": default_accel / 2,
#         "infill_acc": default_accel,
#         "x_max_acc": default_accel,
#         "y_max_acc": default_accel,
#         "z_max_acc": default_accel / 40,
#         "e_max_acc": default_accel,
#         "classic_jerk": False,
#         "default_jerk": default_jerk,
#         "infill_jerk": default_jerk,
#         "default_junction_deviation": round(0.4 * (default_jerk**2 / default_accel), 4),
#         "perimeter_junction_deviation": round(
#             0.4 * (default_jerk**2 / default_accel), 4
#         ),
#         "infill_junction_deviation": round(0.4 * (infill_jerk**2 / default_accel), 4),
#         "travel_junction_deviation": round(0.4 * (default_jerk**2 / default_accel), 4),
#     },
#     "misc_default_settings": {
#         "enable_active_temperature_control": True,
#         "add_brim": True,
#         "brim_distance_to_print_mm": 2,
#         "brim_num_contours": 3,
#         "enable_z_lift": True,
#         "z_lift_mm": 1,
#         "enable_travel_straight": True,
#         "extruder_swap_zlift_mm": 0.2,
#         "extruder_swap_retract_length_mm": 6.5,
#         "extruder_swap_retract_speed_mm_per_sec": 25,
#     },
#     "additional_features": {
#         "use_per_path_accel": False,
#         "volumetric_flow": round(default_printing_speed*default_layer_height*default_nozzle_diameter, 2),
#         "auto_bed_leveling": False,
#         "reload_bed_mesh": False,
#     },
# }


# #features for the Profiles folder
# quality_features = {
#     "layer_thickness_changes": {
#         "z_layer_height_mm": 0.2
#         },
#     "speed_changes": {
#         "print_speed_mm_per_sec": 60,
#         "perimeter_print_speed_mm_per_sec": 30,
#         "cover_print_speed_mm_per_sec": 30,
#         "first_layer_print_speed_mm_per_sec": 20,
#         "travel_speed_mm_per_sec": 80,
#         "priming_mm_per_sec": 40,
#         "retract_mm_per_sec": 40,
#         "speed_multiplier_0": 1,
#     },
# }


# #features for the Materials folder
# materials_features = {
#     "retraction_changes": {
#         "filament_priming_mm": 0.8,
#     },
#     "temperature_changes": {
#         "extruder_temp_degree_c": 210,
#         "bed_temp_degree_c": 60,
#         "chamber_temp_degree_c": 0,
#         "enable_fan": True,
#         "fan_speed_percent": 100,
#         "fan_speed_percent_on_bridges": 100,
#     },
#     "speed_changes": {
#         "print_speed_mm_per_sec": 60,
#         "perimeter_print_speed_mm_per_sec": 45,
#         "cover_print_speed_mm_per_sec": 30,
#         "first_layer_print_speed_mm_per_sec": 20,
#     },
# }

# # list of advanced features that are mostly rescaled values of defining features, hidden by default.
# # Used in main.py to enable/disable their display.
# advanced_features = [
#     "enable_active_temperature_control",
#     "filament_linear_adv_factor",
#     "perimeter_print_speed_mm_per_sec",
#     "cover_print_speed_mm_per_sec",
#     "first_layer_print_speed_mm_per_sec",
#     "travel_speed_mm_per_sec",
#     "enable_travel_straight",
# ]
# advanced_features += [feature for feature in features_dict["retraction_settings"]]
# advanced_features += [
#     feature
#     for category in features_dict
#     for feature in features_dict[category]
#     if (
#         feature.endswith("min")
#         or feature.endswith("max")
#         or feature.startswith("extruder_swap")
#     )
# ]
# advanced_features += [feature for feature in features_dict["additional_features"]]

# #list of features disabled on startup. They may be so because they depend on another feature
# start_as_disabled = [
#     "default_jerk",
#     "infill_jerk",
#     "chamber_temp_degree_c",
#     "chamber_temp_degree_c_min",
#     "chamber_temp_degree_c_max",
#     "reload_bed_mesh"
# ]
# # list of acceleration features. Hidden by default and only accessible when acceleration is enabled in advanced mode.
# accel_features = [feature for feature in features_dict["acceleration_settings"]]
