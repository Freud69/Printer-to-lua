
# Printer-to-lua

External Python app that allows anyone to generate a basic printer profile for the [Ice-SL Slicer](https://icesl.loria.fr/) by team MFX.
App done as an internship projet for team MFX under 6 weeks. May resume later if not finished in time.


## Acknowledgements

 - [Textual](https://textual.textualize.io/) powers the entirety of the app through a seamless console-embedded UI with reactive components. Particularly useful to get a live-view of what your settings will generate. Waiting for _textual-web_ to integrate client-side copy-to-clipboard and file saving to upgrade this app into a web-app.
 - The [Ice-SL printers repository](https://github.com/shapeforge/icesl-printers) with updated access to supported printers'profiles.
 - The [Ice-SL printer documentation ](https://gitlab.inria.fr/mfx/icesl-documentation/-/wikis/Printer-profile) helped finding the general template for each file.

## Features ✨

- Reactive and aesthetic UI for your console
- Live console to see the result
- Generate features.lua file
- Generate quality profiles
- Generate materials profiles
- Generate main printer.lua file, used by IceSL to generate the G-code.

## Requirements

Requirements available in requirements.txt file. Run the following pip query inside the project's folder to install all of them at once:

```bash
  pip install -r requirements.txt
```

## Use
To start the app, just do the following in a terminal inside the project's folder:
```bash
  python main.py
```
Files you generate will be saved in the same directory.

### features.lua
The Features tab allows for the `features.lua` file creation; On the left, input fields. On the right, a log visualizer that shows you the result once you create the file.
First, input a _printer name_, otherwise the `Create` Button, as well as the Quality tab, the Materials tab, and the `printer.lua` file creation will all stay disabled. This is also essential as the Profile folder will use the chosen name.

Each input has active validators, originally implemented to check if the values are coherent with each other, but most of them are incomplete as of now. This won't stop you from creating your profile though, as it will only highlight the field's perimeter in red if the value doesn't correspond to default min-max values.

If you want to modify any default value, please check the _dicts folder_ subsection.

### Quality tab and Materials Tab
Those are overall similar to the `features.lua` tab. Changing the quality/material selection will also yield default values to each field, for your convenience.

### printer.lua
This tab contains interactive code editing areas, with essential functions for `printer.lua` in it. It uses _tree-sitter_ to emulate the highlights, although this app uses the Python preset due to the lua _tree-sitter_ being deprecated and no longer updated.

Please note that each code snippet is automatically generated thanks to the `Features Tab`; For instance,
```lua
--set limits
    output('M201 X' .. x_max_acc .. ' Y' .. y_max_acc .. ' Z' .. z_max_acc .. ' E' .. e_max_acc .. ' ; sets maximum accelerations, mm/sec^2')
    output('M203 X' .. x_max_speed .. ' Y' .. y_max_speed .. ' Z' .. z_max_speed .. ' E' .. e_max_speed .. ' ; sets maximum feedrates, mm/sec')
    output('M204 P' .. default_acc .. ' R' .. e_prime_max_acc .. ' T' .. default_acc .. ' ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2')
    output('M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec')
```
is only generated when acceleration is enabled.

Despite this, the code editing areas remain modifiable and any change will be passed down to the actual final file.

### dicts folder
The _dicts_ folder contains every single default data used by the App, all gathered in dictionaries. The `features_data.py` file contains every feature and its default values, as well as if it is hidden or disabled on the UI on startup.

To update any default value, modify the tuples/default variables in `features_data.py` 's dictionaries. They have the following format:
```python
(default_value, type, min_value, max_value, isHidden, isDisabled)
```
Min and max values will be used by the validators to ensure the input values are within acceptable range. Some of these values may seem redundant as min and max values also exist within the implemented variables used by _IceSl_.


This also specifically concerns `printer.lua` default functions used by IceSL for each firmware (in each corresponding really well named dicts), with some of them being composed of many sub-entries. Those functions normally have their own dictionaries while others are in the  firmware_function_dict_.

Here is an example of a footer snipper for the Klipper firmware:
```python
klipper_footer_dict = {
  'start_footer':"""
function footer()
  -- called to create the footer of the G-Code file.
output('END_PRINT')
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
    output('; set velocity / acceleration limits')
    output('SET_VELOCITY_LIMIT VELOCITY=' .. (x_max_speed + y_max_speed)/2 .. ' ACCEL=' .. (x_max_acc + y_max_acc)/2 .. ' ACCEL_TO_DECEL=' .. ((x_max_acc + y_max_acc)/2)/2 .. ' SQUARE_CORNER_VELOCITY=' .. round(jerk_to_scv(default_jerk),2) )
  """,

  'end_footer':"""
end
  """
  }
```
.
They also have, in `main.py`, a designated _reactive_ attribute that stores their value, as wella as a  _refresh_ function to update their writing in the final file. If you want to modify the order of sub-entries'writing or want to delete some of them, do not forget to also delete the line in the corresponding _refresh_ function. For example:
```python
self.featurecode += 'self.header_dict['end_header']'
```
is the ending code of the header function.


## TODOs
- Implement file opening.
- Revamp purge line script according to the printer's bed size.
- Include support for circular bed in printer.lua file.
- Pack the app for easy download and use.
- Integrate web SSH support.
