
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
The Features tab allows for the `features.lua` file creation;
First, input a _printer name_, otherwise the `Create` Button, as well as the Quality tab, the Materials tab, and the `printer.lua` file creation will all stay disabled. This is also essential as the Profile folder will use the chosen name.

Each input has active validators, originally implemented to check if the values are coherent with each other, but most of them are incomplete as of now. This won't stop you from creating your profile though, as it will only highlight the field's perimeter in red if the value doesn't correspond to default min-max values.

If you want to modify any default value, please check the _dicts folder_ subsection.

### Quality tab and Materials Tab
Those are overall similar to the `features.lua` tab. Changing the quality/material selection will also yield default values to each field, for your convenience.

### printer.lua
This tab contains interactive code editor zones, with essential function for `printer.lua` in it. It uses _tree-sitter_ to emulate the highlights, although this app uses the Python preset due to the lua _tree-sitter_ being deprecated and no longer updated.

### dicts folder
In general, the _dicts_ folder contains every single default data used by the App, all gathered in dictionaries. The `features_data.py` file contains every feature and its default values, as well as if it is hidden or disabled on the UI on startup.

To update any default value, modify the tuples/default variables in `features_data.py` 's dictionaries. They have the following format:
```python
(default_value, type, min_value, max_value, isHidden, isDisabled)
```
Min and max values will be used by the validators to ensure the input values are within acceptable range. Some of these values may seem redundant as min and max values also exist within the implemented variables used by _IceSl_.

This specifically concerns `printer.lua` default functions used by IceSL, with some of them being composed of many sub-entries. Those functions normally have their own dictionaries, and have, in `main.py`, a designated _reactive_ attribute that stores their value, as wella as a  _refresh_ function to update their writing in the final file. If you want to modify the order of sub-entries'writing or want to delete some of them, do not forget to also delete the line in the corresponding _refresh_ function. For example:
```python
self.featurecode += 'self.header_dict['end_header']'
```
is the ending code of the header function.


## TODOs

- Include support for circular bed in printer.lua file.
- Include support for multiple extruders.
- Pack the app for easy download and use.
- Integrate web SSH support.
