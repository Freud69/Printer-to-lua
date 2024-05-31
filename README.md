
# Printer-to-lua

External Python app that allows anyone to generate a basic printer profile for the [Ice-SL Slicer](https://icesl.loria.fr/) by team MFX.



## Acknowledgements

 - [Textual](https://textual.textualize.io/) powers the entirety of the app through a seamless console-embedded UI with reactive components. Particularly useful to get a live-view of what your settings will generate.
 - The [Ice-SL printers repository](https://github.com/shapeforge/icesl-printers) with updated access to supported printers'profiles.
 - [Ice-SL printer documentation ](https://gitlab.inria.fr/mfx/icesl-documentation/-/wikis/Printer-profile)


## Requirements

requirements available in requirements.txt file. Run the following pip query inside the project's folder:

```bash
  pip install -r requirements.txt
```
## TODOs

-Include support for circular bed in printer.lua file.
-Include support for multiple extruders.
-Pack the app for easy download and use.
