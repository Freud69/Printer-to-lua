--Printer functions for Anet ET4 Pro
--Created on 06/15/24
 
--Firmware: 0 = Marlin; 1 = RRF; 2 = Klipper;
firmware = 0
output(';Layer height: ' .. round(z_layer_height_mm, 2)) 
output(';Generated with ' .. slicer_name .. ' ' .. slicer_version .. '\n') 
 
--//////////////////////////////////////////////////Defining main variables
extruder_e = 0
exruder_e_restart = 0
current_z = 0.0
changed_frate = false
processing = false
current_extruder = 0
current_frate = 0
current_fan_speed = -1
craftware_debug = true

path_type = {
--{ 'default',    'Craftware'}
  { ';perimeter',  ';segType:Perimeter' },
  { ';shell',      ';segType:HShell' },
  { ';infill',     ';segType:Infill' },
  { ';raft',       ';segType:Raft' },
  { ';brim',       ';segType:Skirt' },
  { ';shield',     ';segType:Pillar' },
  { ';support',    ';segType:Support' },
  { ';tower',      ';segType:Pillar'}
}

--//////////////////////////////////////////////////Main Functions - called by IceSL 
--################################################## HEADER & FOOTER 
function header()

    -- called to create the header of the G-Code file.

    output('G21 ; set units to millimeters')
    output('G90 ; use absolute coordinates')
    output('M82 ; extruder absolute mode') --constant
        
    --set limits
    output('M201 X' .. x_max_acc .. ' Y' .. y_max_acc .. ' Z' .. z_max_acc .. ' E' .. e_max_acc .. ' ; sets maximum accelerations, mm/sec^2')
    output('M203 X' .. x_max_speed .. ' Y' .. y_max_speed .. ' Z' .. z_max_speed .. ' E' .. e_max_speed .. ' ; sets maximum feedrates, mm/sec')
    output('M204 P' .. default_acc .. ' R' .. e_prime_max_acc .. ' T' .. default_acc .. ' ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2')
    output('M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec')
    
      output('M205 X' .. default_jerk .. ' Y' .. default_jerk .. ' ; sets XY Jerk')
    
    output('')

    output('M109 R' .. extruder_temp_degree_c[extruders[0]] .. ' ; set extruder temp')
    output('M190 S' .. bed_temp_degree_c .. ' ; wait for bed temp')
        
    output('M107')
    output('G28 ; home all without mesh bed level')

        
    --start auto bed leveling
    output('G29 ; auto bed leveling')
    output('G0 F' .. travel_speed_mm_per_sec * 60 .. 'X0 Y0 ; back to the origin to begin the purge')
        
    output('M109 S' .. extruder_temp_degree_c[extruders[0]] .. ' ; wait for extruder temp')

    output('')
    --set Linear Advance k-factor
    output('M900 K' .. filament_linear_adv_factor .. ' ; Linear/Pressure advance')

    current_frate = travel_speed_mm_per_sec * 60
    changed_frate = true

end
        -----------------------
function footer()
    --called to create the footer of the G-Code file.

    output('')
    output('G4 ; wait')
    output('M104 S0 ; turn off temperature')
    output('M140 S0 ; turn off heatbed')
  

    output('M107 ; turn off fan')
    output('G28 X Y ; home X and Y axis')
    output('G91')
    output('G0 Z 10') -- move in Z to clear space between print and nozzle
    output('G90')
    output('M84 ; disable motors')
    output('')
  
    --set limits back to original values.
    output('M201 X' .. x_max_acc .. ' Y' .. y_max_acc .. ' Z' .. z_max_acc .. ' E' .. e_max_acc .. ' ; sets maximum accelerations, mm/sec^2')
    output('M203 X' .. x_max_speed .. ' Y' .. y_max_speed .. ' Z' .. z_max_speed .. ' E' .. e_max_speed .. ' ; sets maximum feedrates, mm/sec')
    output('M204 P' .. default_acc .. ' R' .. e_prime_max_acc .. ' T' .. default_acc .. ' ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2')
    output('M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec')
    
      output('M205 J' .. default_junction_deviation .. ' ; sets Junction Deviation')
    
end
  

--################################################## COMMENT 
function comment(text)
  --[[
    called when outputting a comment "text".
    ]]
    output('; ' .. text)
end

-----------------------
--################################################## LAYER
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
-----------------------
function layer_stop()
--called at the end of a layer.

  extruder_e_restart = extruder_e
  output('G92 E0')
  output('; </layer>')
                                  
end
                                  
-----------------------
--################################################## EXTRUDER
function extruder_start()
  --called before extruding.

end
-----------------------
function extruder_stop()
  --called after extruding.

end
-----------------------
function select_extruder(extruder)
--[[
    called when setting-up the extruder "extruder". This function is called for each available extruder at 
    the beginning of the G-Code and once for the first used extruder in the print. 
    After this, IceSL calls "swap_extruder".
    ]]
    -- hack to work around not beeing a lua global""",

  
    local n = nozzle_diameter_mm_0
  
    local x_pos = 0.1
    local y_pos = 20
    local z_pos = 0.3
  
    local l1 = 200 -- length of 1st purge line
    local l2 = 200 -- length of 2nd purge line
  
    local w = n * 1.2 -- width of the purge line
  
  
    local e_value = 0.0
  
    output('\n; purge extruder')
    output('G0 F6000 X' .. f(x_pos) .. ' Y' .. f(y_pos) ..' Z' .. f(z_pos))
    output('G92 E0')
  
    y_pos = y_pos + l1
    e_value = round(e_from_dep(l1, w, z_pos, extruder),2)
    output('G1 F1500 Y' .. f(y_pos) .. ' E' .. e_value .. '   ; draw 1st line') -- purge start
  
    x_pos = x_pos + n*0.75
    output('G1 F5000 X' .. f(x_pos) .. '   ; move a little to the side')
  
    y_pos = y_pos - l2
    e_value = e_value + round(e_from_dep(l2, w, z_pos, extruder),2)
    output('G1 F1000 Y' .. f(y_pos) .. ' E' .. e_value .. '  ; draw 2nd line') -- purge end
    output('G92 E0')
    output('; done purging extruder\n')
  
    current_extruder = extruder
    current_frate = travel_speed_mm_per_sec * 60
    changed_frate = true
  end
  -----------------------
function swap_extruder(ext1,ext2,x,y,z)
  --[[
    called when swapping extruder 'ext1' to 'ext2' at position x,y,z.
    ]]
end
-----------------------
--################################################## MOVEMENTS
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
-----------------------
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
-----------------------
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
-----------------------
function move_xyz(x,y,z)      
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
  -----------------------
function move_xyze(x,y,z,e)
  --[[
    called when traveling to "x,y,z" while extruding to value "e".
    ]]
    extruder_e = e
  
    local e_value = extruder_e - extruder_e_restart
  
    if processing == false then
        processing = true
  
        p_type = 2
  
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
            then
              output('M204 P' .. perimeter_acc)
              if classic_jerk == true then
                output('M205 X' .. default_jerk .. ' Y' .. default_jerk)
              else
                output('M205 J' .. perimeter_junction_deviation)
              
      elseif path_is_infill                     
            then
              output('M204 P' .. infill_acc)
              if classic_jerk == true then
                output('M205 X' .. infill_jerk .. ' Y' .. infill_jerk)
              else
                output('M205 J' .. infill_junction_deviation)
              
      elseif (path_is_raft or path_is_brim or path_is_shield or path_is_support or path_is_tower)
            then
              output('M204 P' .. default_acc)
              if classic_jerk == true then
                output('M205 X' .. default_jerk .. ' Y' .. default_jerk)
              else
                output('M205 J' .. default_junction_deviation)
              
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

-----------------------
--################################################## PROGRESS 
function progress(percent)
  output('M73 P' .. percent)
end
-----------------------
--################################################## SET
function set_feedrate(rate)
  --[[
    called when setting the feed-rate of the printer to "rate".
    ]]
    if rate ~= current_frate then
      current_frate = rate
      changed_frate = true
    end
end
-----------------------
function set_fan_speed(speed)
  --[[
    called when setting the part cooling fan velocity to "speed" (%).
    ]]
    if speed ~= current_fan_speed then
      output('M106 S'.. math.floor(255 * speed/100))
      current_fan_speed = speed
    end
end
-----------------------
function set_extruder_temperature(extruder,temperature)
  --[[
    called when setting the extruder "extruder" temperature to "temperature".
    ]]
    output('M104 S' .. temperature)
end
-----------------------
--################################################## WAIT
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
-----------------------
--################################################## MIXING PARAMETERS
function set_and_wait_extruder_temperature(extruder,temperature)
  --[[
    called when setting the extruder "extruder" temperature to "temperature" while waiting. 
    Used when printing with multiple extruders.
    ]]
    output('M109 S' .. temperature)
end
-----------------------
function set_mixing_ratios(ratios)
  --[[   
    called when setting the mixing ratios of each filament fed onto the mixing extruder; 
    "ratios" is a table containing the ratio for each filament (the add up to 1). 
    This function is only called when using color mixing.
    ]]
end        
-----------------------
 

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

