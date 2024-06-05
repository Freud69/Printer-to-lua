klipper_function_dict = {
    "COMMENT": {
        "comment": """ 
function comment(text)
  --[[
    called when outputting a comment "text".
    ]]
    output('; ' .. text)
end

"""},
    "LAYER": {
        "layer_start": """
function layer_start(zheight)
  --called at the start of a layer at height "zheight" (mm).
                                   
    output('; <layer ' .. layer_id .. '>')
    local frate = 100
    if layer_id == 0 then
      frate = 600
      if not layer_spiralized then
        output('G0 F' .. frate ..' Z' .. ff(zheight))
      end
    else
      if not layer_spiralized then
        output('G0 F' .. frate ..' Z' .. ff(zheight))
      end
    end
    current_frate = frate
    changed_frate = true
end
""",
        "layer_stop": """
function layer_stop()
--called at the end of a layer.

  extruder_e_restart = extruder_e
  output('G92 E0')
  output('; </layer>')
                                  
end
                                  
""",
    },
    "EXTRUDER": {
        "extruder_start": """
function extruder_start()
  --called before extruding.

end
""",
        "extruder_stop": """
function extruder_stop()
  --called after extruding.

end
""",
        "select_extruder": """
function select_extruder(extruder)
--[[
    called when setting-up the extruder "extruder". This function is called for each available extruder at 
    the beginning of the G-Code and once for the first used extruder in the print. 
    After this, IceSL calls "swap_extruder".
    ]]
    -- hack to work around not beeing a lua global""",
        "swap_extruder": """
function swap_extruder(ext1,ext2,x,y,z)
  --[[
    called when swapping extruder 'ext1' to 'ext2' at position x,y,z.
    ]]
end
""",
    },
    "MOVEMENTS": {
        "prime": """
function prime(extruder,e)
  --[[
    called when priming from value "e" with extruder "extruder". 
    This function must return the absolute value of the E-axis after priming.
    ]]
    output(';prime')
    local len   = filament_priming_mm[extruder]
    local speed = priming_mm_per_sec[extruder] * 60
    output('G1 F' .. speed .. ' E' .. ff(e + len - extruder_e_restart))
    extruder_e = e + len
    current_frate = speed
    changed_frate = true
    return e + len
end
""",
        "retract": """
function retract(extruder,e)
  --[[
    called when retracting from value "e" with extruder "extruder". 
    This function must return the absolute value of the-E axis after retracting.
    ]]
    output(';retract')
    local len   = filament_priming_mm[extruder]
    local speed = retract_mm_per_sec[extruder] * 60
    output('G1 F' .. speed .. ' E' .. ff(e - len - extruder_e_restart))
    extruder_e = e - len
    current_frate = speed
    changed_frate = true
    return e - len
  end
""",
        "move_e": """
function move_e(e)
  --[[
    called when moving the E-axis to value "e" with the current extruder.
    ]]
    extruder_e = e
  
    local e_value =  extruder_e - extruder_e_restart
  
    if changed_frate == true then
      output('G1 F' .. current_frate .. ' E' .. ff(e_value))
      changed_frate = false
    else
      output('G1 E' .. ff(e_value))
    end
end
""",
        "move_xyz": """
  --[[
    called when traveling to "x,y,z".
    ]]
    if processing == true then
        processing = false
        output(';travel')
        if use_per_path_accel then
            output('M204 S' .. default_acc)
        end
    end
  
    if z == current_z then
        if changed_frate == true then
            output('G0 F' .. current_frate .. ' X' .. f(x) .. ' Y' .. f(y))
            changed_frate = false
        else
            output('G0 X' .. f(x) .. ' Y' .. f(y))
        end
    else
        if changed_frate == true then
            output('G0 F' .. current_frate .. ' X' .. f(x) .. ' Y' .. f(y) .. ' Z' .. ff(z))
            changed_frate = false
        else
            output('G0 X' .. f(x) .. ' Y' .. f(y) .. ' Z' .. ff(z))
        end
        current_z = z
    end
end
""",
        "move_xyze": """
  --[[
    called when traveling to "x,y,z" while extruding to value "e".
    ]]
    extruder_e = e
  
    local e_value = extruder_e - extruder_e_restart
  
    if processing == false then
      processing = true
      local p_type = 1 -- default paths naming
      if craftware_debug then p_type = 2 end
      if      path_is_perimeter then output(path_type[1][p_type])
      elseif  path_is_shell     then output(path_type[2][p_type])
      elseif  path_is_infill    then output(path_type[3][p_type])
      elseif  path_is_raft      then output(path_type[4][p_type])
      elseif  path_is_brim      then output(path_type[5][p_type])
      elseif  path_is_shield    then output(path_type[6][p_type])
      elseif  path_is_support   then output(path_type[7][p_type])
      elseif  path_is_tower     then output(path_type[8][p_type])
    end
  
      -- acceleration management
    if use_per_path_accel then
      if     path_is_perimeter or path_is_shell 
            then set_acceleration(perimeter_acc, default_jerk)
      elseif path_is_infill                     
            then set_acceleration(infill_acc, infill_jerk)
      elseif (path_is_raft or path_is_brim or path_is_shield or path_is_support or path_is_tower)
            then set_acceleration(default_acc, default_jerk)
      end
    end
end
  
    if z == current_z then
      if changed_frate == true then
        output('G1 F' .. current_frate .. ' X' .. f(x) .. ' Y' .. f(y) .. ' E' .. ff(e_value))
        changed_frate = false
      else
        output('G1 X' .. f(x) .. ' Y' .. f(y) .. ' E' .. ff(e_value))
      end
    else
      if changed_frate == true then
        output('G1 F' .. current_frate .. ' X' .. f(x) .. ' Y' .. f(y) .. ' Z' .. ff(z) .. ' E' .. ff(e_value))
        changed_frate = false
      else
        output('G1 X' .. f(x) .. ' Y' .. f(y) .. ' Z' .. ff(z) .. ' E' .. ff(e_value))
      end
      current_z = z
    end
end
""",
    },
    "PROGRESS": {
        "progress": """ 
function progress(percent)
  output('M73 P' .. percent)
end

"""
    },
    "SET": {
        "set_feedrate": """
function set_feedrate(rate)
  --[[
    called when setting the feed-rate of the printer to "rate".
    ]]
    if rate ~= current_frate then
      current_frate = rate
      changed_frate = true
    end
end
""",
        "set_fan_speed": """
function set_fan_speed(speed)
  --[[
    called when setting the part cooling fan velocity to "speed" (%).
    ]]
    if speed ~= current_fan_speed then
      output('M106 S'.. math.floor(255 * speed/100))
      current_fan_speed = speed
    end
end
""",
        "set_extruder_temperature": """
function set_extruder_temperature(extruder,temperature)
  --[[
    called when setting the extruder "extruder" temperature to "temperature".
    ]]
    output('M104 S' .. temperature)
end
""",
    },
    "WAIT": {
        "wait": """
function wait(sec,x,y,z)
  --[[
    called when the parameter "enable_min_layer_time" is set to true
    and the printing time for the layer is less than "min_layer_time_sec". 
    "sec" is the remaining time to achieve "min_layer_time_sec" and 
    "x,y,z" is where IceSL expects the head to be after the wait.
    ]]
    output("; WAIT --" .. sec .. "s remaining" )
    output("G0 F" .. travel_speed_mm_per_sec .. " X10 Y10")
    output("G4 S" .. sec .. "; wait for " .. sec .. "s")
    output("G0 F" .. travel_speed_mm_per_sec .. " X" .. f(x) .. " Y" .. f(y) .. " Z" .. ff(z))
  end
""",
    },
    "MIXING PARAMETERS": {
        "set_and_wait_extruder_temperature": """
function set_and_wait_extruder_temperature(extruder,temperature)
  --[[
    called when setting the extruder "extruder" temperature to "temperature" while waiting. 
    Used when printing with multiple extruders.
    ]]
    output('M109 S' .. temperature)
end
""",
        "set_mixing_ratios": """
function set_mixing_ratios(ratios)
  --[[   
    called when setting the mixing ratios of each filament fed onto the mixing extruder; 
    "ratios" is a table containing the ratio for each filament (the add up to 1). 
    This function is only called when using color mixing.
    ]]
end        
""",
    },
}