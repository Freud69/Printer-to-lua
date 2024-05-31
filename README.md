
# Printer-to-lua

External Python app that allows anyone to generate a basic printer profile for the [Ice-SL Slicer](https://icesl.loria.fr/) by team MFX.
Project done as an internship project for team MFX under 6 weeks. May resume later if not finished in time.


## Acknowledgements

 - [Textual](https://textual.textualize.io/) powers the entirety of the app through a seamless console-embedded UI with reactive components. Particularly useful to get a live-view of what your settings will generate. Waiting for _textual-web_ to integrate client-side copy-to-clipboard and file saving to upgrade this app into a web-app.
 - The [Ice-SL printers repository](https://github.com/shapeforge/icesl-printers) with updated access to supported printers'profiles.
 - The [Ice-SL printer documentation ](https://gitlab.inria.fr/mfx/icesl-documentation/-/wikis/Printer-profile) helped finding the general template for each file.

## Features

- Reactive and aesthetic UI for your console
- Live console to see the result
- Generate features.lua file
- Generate quality profiles
- Generate materials profiles
- Generate main printer.lua file, used by the IceSL to generate the G-code.
- 
## Requirements

requirements available in requirements.txt file. Run the following pip query inside the project's folder:

```bash
  pip install -r requirements.txt
```
## TODOs

- Include support for circular bed in printer.lua file.
- Include support for multiple extruders.
- Pack the app for easy download and use.
- Integrate web SSH support.
