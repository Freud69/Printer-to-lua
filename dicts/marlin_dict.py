#This dictionary contains the lua functions for the Marlin firmware
#Header, Footer, Select Extruder, Move XYZ, Move XYZE have a separate dictionary as they depend on the Features tab
#Each step is a separate entry in the dictionary.
#If you modify the functions, make sure to update the python file accordingly
#The functions are stored in a dictionary with the key as the function name and the value as the function definition
#Functions in functions_dict are not dependent on the Features tab

marlin_header_dict = {
    'start_header':"""function header()

    -- called to create the header of the G-Code file.

    output('G21 ; set units to millimeters')
    output('G90 ; use absolute coordinates')
    output('M82 ; extruder absolute mode') --constant
        """,
      
    'enable_acceleration':"""
    --set limits
    output('M201 X' .. x_max_acc .. ' Y' .. y_max_acc .. ' Z' .. z_max_acc .. ' E' .. e_max_acc .. ' ; sets maximum accelerations, mm/sec^2')
    output('M203 X' .. x_max_speed .. ' Y' .. y_max_speed .. ' Z' .. z_max_speed .. ' E' .. e_max_speed .. ' ; sets maximum feedrates, mm/sec')
    output('M204 P' .. default_acc .. ' R' .. e_prime_max_acc .. ' T' .. default_acc .. ' ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2')
    output('M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec')
    """ ,
  'jerk_true':"""
      output('M205 X' .. default_jerk .. ' Y' .. default_jerk .. ' ; sets XY Jerk')
    """ ,
  'jerk_false':"""
      output('M205 J' .. default_junction_deviation .. ' ; sets Junction Deviation')
    """ ,
      
    'temp_setup':"""
    output('')
    output('T'.. current_extruder)
    output('M104 S' .. extruder_temp_degree_c[extruders[0]] .. ' ; set extruder temp')
    output('M190 S' .. bed_temp_degree_c .. ' ; wait for bed temp')
    output('M109 T' .. current_extruder.. ' S' .. extruder_temp_degree_c[extruders[0]] .. ' ; set extruder temp')
        """,

    'heated_chamber':"""
    --activate heated chamber
    output('M141 S' .. chamber_temp_degree_c .. ' ; set and wait chamber temperature')
        """,
    
    'home_all':"""
    output('M107')
    output('G28 ; home all without mesh bed level')

        """,
    
    'auto_bed_leveling':"""
    --start auto bed leveling
    output('G29 ; auto bed leveling')
    output('G0 F' .. travel_speed_mm_per_sec * 60 .. 'X0 Y0 ; back to the origin to begin the purge')

        """,
    
    'auto_bed_leveling_and_reload_bed_mesh':"""
    --start auto bed leveling and reload previous bed mesh
    output('M420 S1 ; enable bed leveling (was disabled y G28)')
    output('M420 L ; load previous bed mesh')
        """,

    'purge_extruder': """
    --purge extruder
    output('T'.. current_extruder .. '; select the current extruder')
    output('G0 F6000 X0.100 Y20.000 Z0.300')
    output('G92 E0')
    output('G1 F1500 Y200.000 E18.8   ; draw 1st line')
    output('G1 F5000 X0.400   ; move a little to the side')
    output('G1 F1000 Y20.000 E37.6  ; draw 2nd line')
    output('G92 E0')
    output('; done purging extruder')
        """,
    
    'end_header':"""
    output('M109 T'.. current_extruder..' S' .. extruder_temp_degree_c[extruders[0]] .. ' ; wait for extruder temp')

    output('')
    --set Linear Advance k-factor
    output('M900 K' .. filament_linear_adv_factor .. ' ; Linear/Pressure advance')

    current_frate = travel_speed_mm_per_sec * 60
    changed_frate = true

end
        """     
}

marlin_footer_dict = {
  'start_footer':"""
function footer()
    --called to create the footer of the G-Code file.

    output('')
    output('G4 ; wait')
    output('M104 T'.. current_extruder..' S0 ; turn off temperature')
    output('M140 S0 ; turn off heatbed')
  """,

  'heated_chamber': """
    output('M141 S0 ; turn off heated chamber')
  """,

  'home_all':"""

    output('M107 ; turn off fan')
    output('G28 X Y ; home X and Y axis')
    output('G91')
    output('G0 Z 10') -- move in Z to clear space between print and nozzle
    output('G90')
    output('M84 ; disable motors')
    output('')
  """,
    
  'enable_acceleration':"""
    --set limits back to original values.
    output('M201 X' .. x_max_acc .. ' Y' .. y_max_acc .. ' Z' .. z_max_acc .. ' E' .. e_max_acc .. ' ; sets maximum accelerations, mm/sec^2')
    output('M203 X' .. x_max_speed .. ' Y' .. y_max_speed .. ' Z' .. z_max_speed .. ' E' .. e_max_speed .. ' ; sets maximum feedrates, mm/sec')
    output('M204 P' .. default_acc .. ' R' .. e_prime_max_acc .. ' T' .. default_acc .. ' ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2')
    output('M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec')
    """ ,
  'jerk_true':"""
      output('M205 X' .. default_jerk .. ' Y' .. default_jerk .. ' ; sets XY Jerk')
    """ ,
  'jerk_false':"""
      output('M205 J' .. default_junction_deviation .. ' ; sets Junction Deviation')
    """ ,

  'end_footer':"""
end
  """
}
marlin_select_extruder_dict = {
  'start_select_extruder':'''
function select_extruder(extruder)
--[[
    called when setting-up the extruder "extruder". This function is called for each available extruder at 
    the beginning of the G-Code and once for the first used extruder in the print. 
    After this, IceSL calls "swap_extruder".
    ]]
    -- hack to work around not beeing a lua global""",

  ''',

  'multi_extruders':"""
    local n = nozzle_diameter_mm[extruder]

  """,

  'solo_extruder':"""
    local n = nozzle_diameter_mm_0
  """,

  'end_select_extruder':"""
    local x_pos = 0.1
    local y_pos = 20
    local z_pos = 0.3
  
    local l1 = 200 -- length of 1st purge line
    local l2 = 200 -- length of 2nd purge line
  
    local w = n * 1.2 -- width of the purge line
  
  
    local e_value = 0.0
  
    output('\\n; purge extruder')
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
    output('; done purging extruder\\n')
  
    current_extruder = extruder
    current_frate = travel_speed_mm_per_sec * 60
    changed_frate = true
  end
  """
}

marlin_move_xyz_dict = {
  'start_move_xyz':'''
function move_xyz(x,y,z)      
  --[[
    called when traveling to "x,y,z".
    ]]
    if processing == true then
        processing = false
        output(';travel')
  ''',

  'use_per_path_accel':'''
        output('M204 S' .. default_acc)

  ''',

  'end_move_xyz':'''
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
  '''
}

marlin_move_xyze_dict = {
  'start_move_xyze':'''
function move_xyze(x,y,z,e)
  --[[
    called when traveling to "x,y,z" while extruding to value "e".
    ]]
    extruder_e = e
  
    local e_value = extruder_e - extruder_e_restart
  
    if processing == false then
        processing = true
  ''',

  'craftware_debug_true':'''
        p_type = 2
  ''',

  'craftware_debug_false':'''
        p_type = 1
  ''',

  'path_type':'''
        if      path_is_perimeter then output(path_type[1][p_type])
        elseif  path_is_shell     then output(path_type[2][p_type])
        elseif  path_is_infill    then output(path_type[3][p_type])
        elseif  path_is_raft      then output(path_type[4][p_type])
        elseif  path_is_brim      then output(path_type[5][p_type])
        elseif  path_is_shield    then output(path_type[6][p_type])
        elseif  path_is_support   then output(path_type[7][p_type])
        elseif  path_is_tower     then output(path_type[8][p_type])
      end
    end
  ''',

  'use_per_path_accel':'''
-- acceleration management
      if     path_is_perimeter or path_is_shell 
            then
              output('M204 P' .. perimeter_acc)
              if classic_jerk == true then
                output('M205 X' .. default_jerk .. ' Y' .. default_jerk)
              else
                output('M205 J' .. perimeter_junction_deviation)
              end
      elseif path_is_infill                     
            then
              output('M204 P' .. infill_acc)
              if classic_jerk == true then
                output('M205 X' .. infill_jerk .. ' Y' .. infill_jerk)
              else
                output('M205 J' .. infill_junction_deviation)
              end
      elseif (path_is_raft or path_is_brim or path_is_shield or path_is_support or path_is_tower)
            then
              output('M204 P' .. default_acc)
              if classic_jerk == true then
                output('M205 X' .. default_jerk .. ' Y' .. default_jerk)
              else
                output('M205 J' .. default_junction_deviation)
              end
      end

  ''',

  'end_move_xyze':'''
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

'''
}

marlin_function_dict = {
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
""",

        'swap_extruder': '''
function swap_extruder(ext1,ext2,x,y,z)
  --[[
    called when swapping extruder 'ext1' to 'ext2' at position x,y,z.
    ]]
  output('\\n;swap_extruder')
    extruder_e_swap[ext1] = extruder_e_swap[ext1] + extruder_e[ext1] - extruder_e_reset[ext1]

    -- swap extruder
    output('G92 E0.0')
    output('T' .. ext2)
    output('G92 E0.0\\n')

    current_extruder = ext2
    extruder_changed = true
    current_frate = travel_speed_mm_per_sec * 60
    changed_frate = true
end
'''
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

""",
        "move_xyze": """

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