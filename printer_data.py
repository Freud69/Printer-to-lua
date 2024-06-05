

main_variables = {
    "extruder_e": 0,
    "exruder_e_restart": 0,
    "current_z": 0.0,
    "changed_frate": False,
    "processing": False,
    "current_extruder": 0,
    "current_frate": 0,
    "current_fan_speed": -1,
    "craftware_debug": True,
}

util_functions_text = """
--//////////////////////////////////////////////////Util functions - mainly for unit conversions
function round(number, decimals)
  --[[
    returns a rounded value of "number"
    ]]
  local power = 10^decimals
  return math.floor(number * power) / power
end
-----------------------
function vol_to_mass(volume, density)
  --[[
    converts current volume to mass.
    Used along with the next function to approximate filament consumption."
    ]]
  return density * volume
end
-----------------------
function e_to_mm_cube(filament_diameter, e)
  --[[
    Uses the filament's dimensions and extrusion width to approximate the volume (mm^3)
    Used along with the previous function to approximate filament consumption.
    ]]
  local r = filament_diameter / 2
  return (math.pi * r^2 ) * e
end
-----------------------
-- get the E value (for G1 move) from a specified deposition move
function e_from_dep(dep_length, dep_width, dep_height, extruder)
  --[[
    Yet to be understood
  ]]
  local r1 = dep_width / 2
  local r2 = filament_diameter_mm[extruder] / 2
  local extruded_vol = dep_length * math.pi * r1 * dep_height
  return extruded_vol / (math.pi * r2^2)
end
-----------------------
function jerk_to_junction_deviation(jerk, accel)
  --[[
    Converts Marlin jerk value to junction deviation
    ]]
  return 0.4 * ( (jerk^2) / accel )
end
-----------------------
-- marlin jerk * sqrt(2) = square corner velocity
-- scv = square corner velocity
function scv_to_jerk(scv) 
  --[[
    converts klipper scv value to marlin jerk value
    ]]
  return math.sqrt(2) * scv
end
-----------------------
function jerk_to_scv(jerk)
  --[[
    converts marlin jerk value to klipper scv value
    ]]
  return jerk/math.sqrt(2)
end

"""