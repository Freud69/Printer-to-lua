###Imports
from dicts.marlin_dict import (marlin_header_dict, 
                         marlin_footer_dict, 
                         marlin_select_extruder_dict,
                         marlin_move_xyz_dict,
                         marlin_move_xyze_dict, 
                         marlin_function_dict)

from dicts.rrf_dict import (rrf_header_dict,
                      rrf_footer_dict,
                      rrf_select_extruder_dict,
                      rrf_move_xyz_dict,
                      rrf_move_xyze_dict,
                      rrf_function_dict)

from dicts.klipper_dict import (klipper_header_dict,
                          klipper_footer_dict,
                          klipper_select_extruder_dict,
                          klipper_move_xyz_dict,
                          klipper_move_xyze_dict,
                          klipper_function_dict)

from dicts.tooltips_dict import tooltips

#list and dictionaries of general features
from dicts.features_data import (
                            default_features, features_dict,
                            start_as_disabled, advanced_features,
                            accel_features, quality_features,
                            materials_features
                            )
from dicts.printer_data import main_variables, util_functions_text

from datetime import datetime
import os
from textual.app import App, ComposeResult
from textual import on
from textual.widgets import (
    Header,
    Input,
    Switch,
    Select,
    Button,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
)
from textual.containers import Container, Horizontal, VerticalScroll
from textual.reactive import reactive  # ce qui permet de créer des attributs réactifs pour nos classes
from textual.validation import Function


###Textual GUI
class gui(App):
    """
    Main class for the GUI. It is the main class that will be called by the main.py file.
    It is a subclass of the App class from the Textual library.
    Gives access to reactive variables that can change automatically.\n
    Works by yielding predefined widgets to its compose function, for it to "mount it" and display the app in a terminal.
    """

    ENABLE_COMMAND_PALETTE = False
    # reactive variables. Regularly modified throughout the creation process
    function_dict = marlin_function_dict #dictionary of functions. By default set on marlin. #changed according to FW changes.

    #dictionaries for each highly conditioned functions. They all have a refresh function that actively changes their content.
    header_dict = marlin_header_dict 
    footer_dict = marlin_footer_dict
    select_extruder_dict = marlin_select_extruder_dict
    move_xyz_dict = marlin_move_xyz_dict
    move_xyze_dict = marlin_move_xyze_dict

    featurecode = reactive(                             #Used as a log-text on the right pane
        "Begin by entering your printer's name.",
        always_update=True,
        repaint=True,
        layout=True,
    )  # stores our final result
    printercode = reactive("", always_update=True, repaint=True, layout=True) #same as featurecode but for the printer tab

    extruder_count = reactive(1, always_update=True, repaint=True, layout=True)
    name = reactive("", always_update=True, repaint=True, layout=True)
    firmware = reactive(0, always_update=True, repaint=True, layout=True)
    quality = reactive("low", always_update=True, repaint=True, layout=True)
    material = reactive("pla", always_update=True, repaint=True, layout=True)
    enable_acceleration = reactive(False, always_update=True, repaint=True, layout=True)
    classic_jerk = reactive(False, always_update=True, repaint=True, layout=True)
    heated_chamber = reactive(False, always_update=True, repaint=True, layout=True)
    volumetric_flow = reactive(str(features_dict['additional_features']['volumetric_flow']), 
                               always_update=True, repaint=True, layout=True)
    printing_speed = reactive(str(features_dict['printing_speeds']['print_speed_mm_per_sec']),
                                       always_update=True, repaint=True, layout=True)
    layer_height = reactive(str(features_dict['layer_height']['z_layer_height_mm']), 
                                    always_update=True, repaint=True, layout=True)
    nozzle_diameter = reactive(str(default_features['extruder']['nozzle_diameter_mm_0']), 
                               always_update=True, repaint=True, layout=True)
    
    #custom_features
    auto_bed_leveling = reactive(False, always_update=True, repaint=True, layout=True)
    reload_bed_mesh = reactive(False, always_update=True, repaint=True, layout=True)
    use_per_path_accel = reactive(False, always_update=True, repaint=True, layout=True)

    #reactive variables for the functions in the Printer tab
    craftware_debug = reactive(main_variables["craftware_debug"], always_update=True, repaint=True, layout=True)
    header = reactive("", always_update=True, repaint=True, layout=True)
    footer = reactive("", always_update=True, repaint=True, layout=True)
    comment = reactive(
        function_dict["COMMENT"]["comment"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    layer_start = reactive(
        function_dict["LAYER"]["layer_start"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    layer_stop = reactive(
        function_dict["LAYER"]["layer_stop"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    extruder_start = reactive(
        function_dict["EXTRUDER"]["extruder_start"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    extruder_stop = reactive(
        function_dict["EXTRUDER"]["extruder_stop"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    select_extruder = reactive(
        '',
        always_update=True,
        repaint=True,
        layout=True,
    )
    swap_extruder = reactive(
        function_dict["EXTRUDER"]["swap_extruder"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    prime = reactive(
        function_dict["MOVEMENTS"]["prime"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    retract = reactive(
        function_dict["MOVEMENTS"]["retract"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    move_e = reactive(
        function_dict["MOVEMENTS"]["move_e"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    move_xyz = reactive(
        '',
        always_update=True,
        repaint=True,
        layout=True,
    )
    move_xyze = reactive(
        '',
        always_update=True,
        repaint=True,
        layout=True,
    )
    progress = reactive(
        function_dict["PROGRESS"]["progress"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    set_feedrate = reactive(
        function_dict["SET"]["set_feedrate"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    set_fan_speed = reactive(
        function_dict["SET"]["set_fan_speed"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    set_extruder_temperature = reactive(
        function_dict["SET"]["set_extruder_temperature"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    wait = reactive(
        function_dict["WAIT"]["wait"],
          always_update=True,
          repaint=True,
          layout=True
    )
    set_and_wait_extruder_temperature = reactive(
        function_dict["MIXING PARAMETERS"]["set_and_wait_extruder_temperature"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    set_mixing_ratios = reactive(
        function_dict["MIXING PARAMETERS"]["set_mixing_ratios"],
        always_update=True,
        repaint=True,
        layout=True,
    )
    util_functions = reactive(      #Stores the utility functions
        util_functions_text,
        always_update=True,
        layout=True,
        repaint=True
    )

    TITLE = "Profile to Lua"  # Header's title
    CSS_PATH = "style.tcss"  # Graphic elements are managed through tcss files, much like web css.

    def compose(self) -> ComposeResult:
        """
        Default and mandatory function used by Textual to compose the app's UI.
        Defined by yielding Widgets from Textual to the console.
        When doing so, the terminal is temporarily inacessible and put in a special mode for Textual to exploit it.
        Every widget is identified by its "id" attribute(str).
        """

        yield Header()  # Ui's header
        with TabbedContent():
            # FEATURES TAB
            with TabPane("Features"):
                with Container(
                    classes="app-grid"
                ):  # Overall container. allows for agile widget placements.
                    # Here, it uses the 'grid' format spanning 3 columns and 1 row.
                    with VerticalScroll(
                        classes="features"
                    ):  # left side vertical column, containing the feature fields.

                        # Advanced mode label and button
                        yield Horizontal(  # Horizontal widgets are solely used to contain other subwidgets,
                            # and allows to hide/display all of its children at once.
                            Static(
                                "[b]Advanced mode",
                                classes="feature-text",
                                id="static_advanced_mode",
                            ),  # Static widgets define immutable
                            # renderable objects. mainly used for plain texts
                            Switch(
                                value=False, id="advanced_mode", classes='important_toggle', animate=False
                            ),  # Switch widgets define a toggle-switch with value False and True in accordance
                            # to its state.
                            classes="container",
                        )  # the "classes" attribute is similar to its Web counterpart, refering the css file.

                        # Printer settings
                        yield Static("[b]Printer", classes="label", id="static_printer")

                        yield Horizontal(
                            Static(
                                "Printer's name",
                                classes="feature-text",
                                id="static_name",
                            ),
                            # Input widgets define an input field.
                            # its "type" attribute allows for active input restriction (either "text", "number", or "integer")
                            # its value is stored in a "value" attribute,
                            # only accessible through private method "__getattribute__('value')" or publicly through event controls (down below)
                            Input(
                                placeholder="Printer's name",
                                id="name",
                                type="text",
                                max_length=64,
                                valid_empty=False,
                                validators=[Function(isNotSpaces, "empty name")],
                            ),
                            classes="horizontal-layout",
                        )
                        yield Horizontal(
                            Static(
                                "Firmware", classes="feature-text", id="static_firmware"
                            ),
                            # Select widgets define a scrollable field.
                            # its "options" attribute define possible choices through the tuple: ("display name", true_value)
                            # getting the "value" of a Select widget grants the "true_value" variable of the active selection.
                            # It is accessible through private method "__getattribute__('value')" or publicly through event controls.
                            Select(
                                id="firmware",
                                prompt="Firmware",
                                options=[
                                    ("Marlin", 0),
                                    ("Rep Rap", 1),
                                    ("Klipper", 2),
                                ],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        # Build Area Dimensions
                        yield Static(
                            "[b]Build Area Dimensions",
                            classes="label",
                            id="static_build_area_dimensions",
                        )

                        yield Horizontal(
                            Static(
                                "Bed Shape",
                                classes="feature-text",
                                id="static_bed_circular",
                            ),
                            Select(
                                value=False,
                                prompt="bed shape",
                                allow_blank=False,
                                options=[("rectangular", False), ("circular", True)],
                                id="bed_circular",
                            ),
                            classes="container",
                        )
                        bed_radius_input = Input(
                            value=f'{default_features["build_area_dimensions"]["bed_radius"]}',
                            placeholder="bed radius",
                            id="bed_radius",
                            type="number",
                            max_length=4,
                            valid_empty=False,
                        )
                        bed_radius_input.disabled = True
                        bed_radius_widget = Horizontal(
                            Static(
                                "Bed Radius",
                                classes="feature-text",
                                id="static_bed_radius",
                            ),
                            bed_radius_input,
                            classes="horizontal-layout",
                            id="horizontal_bed_radius",
                        )
                        bed_radius_widget.display = False  # Hides the widget.
                        yield bed_radius_widget

                        yield Horizontal(
                            Static(
                                "Bed Size x (mm)",
                                classes="feature-text",
                                id="static_bed_size_x_mm",
                            ),
                            Input(
                                value="310",
                                placeholder="bed size x mm ",
                                id="bed_size_x_mm",
                                type="number",
                                max_length=4,
                                valid_empty=False,
                            ),
                            classes="horizontal-layout",
                        )
                        yield Horizontal(
                            Static(
                                "Bed Size y (mm)",
                                classes="feature-text",
                                id="static_bed_size_y_mm",
                            ),
                            Input(
                                value="310",
                                placeholder="bed size y mm ",
                                id="bed_size_y_mm",
                                type="number",
                                max_length=4,
                                valid_empty=False,
                            ),
                            classes="horizontal-layout",
                        )
                        yield Horizontal(
                            Static(
                                "Bed Size z (mm)",
                                classes="feature-text",
                                id="static_bed_size_z_mm",
                            ),
                            Input(
                                value="350",
                                placeholder="bed size z mm ",
                                id="bed_size_z_mm",
                                type="number",
                                max_length=4,
                                valid_empty=False,
                            ),
                            classes="horizontal-layout",
                        )

                        # Printer Extruder
                        yield Static(
                            "[b]Extruder Settings",
                            classes="label",
                            id="static_extruder_settings",
                        )

                        yield Horizontal(
                            Static(
                                "Extruder count",
                                classes="feature-text",
                                id="static_extruder_count",
                            ),
                            Select(
                                prompt="extruder count",
                                id="extruder_count",
                                options=[(f"{i}", i) for i in range(1, 15)],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        yield Horizontal(
                            Static(
                                "Nozzle Diameter (mm)",
                                classes="feature-text",
                                id="static_nozzle_diameter_mm_0",
                            ),
                            Select(
                                value=0.4,
                                prompt="Nozzle diameter (mm)",
                                id="nozzle_diameter_mm_0",
                                options=[("0.25", 0.25), ("0.4", 0.4), ("0.6", 0.6)],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        yield Horizontal(
                            Static(
                                f"Filament diameter",
                                classes="feature-text",
                                id="static_filament_diameter_mm_0",
                            ),
                            Select(
                                prompt="filament diameter (mm)",
                                id="filament_diameter_mm_0",
                                options=[("1.75", 1.75), ("2.85", 2.85)],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        # loop to generate doublons of extruder settings, in case there are more than one.
                        # maximum number for supported printers is 14 with the Addiform, thus explaining the loop range.
                        for i in range(2, 15):
                            title_nozzle = Static(
                                f"Nozzle Diameter for extruder {i} (mm)",
                                classes="feature-text",
                                id=f"static_nozzle_diameter_mm_{i-1}",
                            )
                            input_field_nozzle = Select(
                                value=0.4,
                                prompt=f"Nozzle diameter for extruder {i} (mm)",
                                id=f"nozzle_diameter_mm_{i-1}",
                                options=[("0.25", 0.25), ("0.4", 0.4), ("0.6", 0.6)],
                                allow_blank=False,
                            )
                            horizontal_nozzle = Horizontal(
                                title_nozzle,
                                input_field_nozzle,
                                classes="horizontal-layout",
                                id=f"horizontal_nozzle_{i-1}",
                            )
                            horizontal_nozzle.display = False
                            yield horizontal_nozzle

                            title_fildiam = Static(
                                f"Filament diameter for extruder {i} (mm)",
                                classes="feature-text",
                                id=f"static_filament_diameter_mm_{i-1}",
                            )
                            input_field_fildiam = Select(
                                value=1.75,
                                prompt=f"filament diameter for extruder {i} (mm)",
                                id=f"filament_diameter_mm_{i-1}",
                                options=[("1.75", 1.75), ("3.0", 3.0)],
                                allow_blank=False,
                            )
                            horizontal_fildiam = Horizontal(
                                title_fildiam,
                                input_field_fildiam,
                                classes="horizontal-layout",
                                id=f"horizontal_fildiam_{i-1}",
                            )
                            horizontal_fildiam.display = False
                            yield horizontal_fildiam

                        fil_adv_fact = Horizontal(
                            Static(
                                "Filament Linear Advance Factor",
                                classes="feature-text",
                                id="static_filament_linear_adv_factor",
                            ),
                            Input(
                                value="0.06",
                                placeholder="filament linear advance factor",
                                id="filament_linear_adv_factor",
                                type="number",
                                max_length=2,
                                valid_empty=False,
                            ),
                            classes="horizontal-layout",
                            id="horizontal_filament_linear_adv_factor",
                        )
                        fil_adv_fact.display = False
                        yield fil_adv_fact

                        # Other parameters. loops through features_dict to create remaining input fields.
                        for category in features_dict:  # category is a key
                            tmp_key_words = [
                                word for word in category.split("_")
                            ]  # List of words in the feature's name.
                            # Used solely for proper text display purposes
                            placeholder_value = ""  # tmp variable used to concatenate the new title altogether.
                            for word in tmp_key_words:
                                placeholder_value += word + " "
                            title_tmp = Static(
                                f"[b]{placeholder_value.title()}",
                                classes="label",
                                id=f"static_{category}",
                            )  # .title() built-in
                            # function uppercases each starting letter.
                            if (
                                category != "acceleration_settings"
                            ):  # acceleration settings is a special case as it is shown only after toggling
                                # "enable acceleration" in advanced mode
                                yield title_tmp
                            else:
                                yield title_tmp
                                # the "enable acceleration toggle-switch"
                                enable_accel = Horizontal(
                                    Static(
                                        "Enable acceleration",
                                        classes="feature-text",
                                        id="static_enable_acceleration",
                                    ),
                                    Switch(value=False, id="enable_acceleration", animate= False),
                                    classes="container",
                                    id="horizontal_enable_acceleration",
                                    
                                )
                                enable_accel.display = False
                                yield enable_accel

                            # Loops through each feature in a category
                            for feature in features_dict[
                                category
                            ]:  # feature is also a key.
                                tmp_feature_words = [
                                    word for word in feature.split("_")
                                ]
                                placeholder_value = ""
                                for word in tmp_feature_words:
                                    if word in ["mm", "c"] and feature.endswith(
                                        word
                                    ):  # temporary solution to decorate units.
                                        # Will find better later.
                                        placeholder_value += f"({word})"
                                    else:
                                        placeholder_value += word + " "
                                if not isinstance(
                                    features_dict[category][feature], bool
                                ):  # non bool- features will yield an Input widget,
                                    # while bools will yield a Switch
                                    feature_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{feature}",
                                    )
                                    feature_input_field = Input(
                                        value=f"{features_dict[category][feature]}",
                                        placeholder=f"{placeholder_value}",
                                        id=f"{feature}",
                                        type="number",
                                        max_length=5,
                                        valid_empty=False,
                                    )
                                    if feature in start_as_disabled:
                                        feature_input_field.disabled = True
                                    feature_horizontal = Horizontal(
                                        feature_text,
                                        feature_input_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{feature}",
                                    )
                                    if (
                                        feature in advanced_features
                                        or feature in accel_features
                                    ):  # features judged too advanced for a beginner
                                        # are by default hidden
                                        feature_horizontal.display = False
                                    yield feature_horizontal

                                else:  # bool features'case
                                    feature_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{feature}",
                                    )
                                    feature_switch_field = Switch(
                                        value=features_dict[category][feature],
                                        id=f"{feature}",
                                        animate= False
                                    )
                                    if feature in start_as_disabled:
                                        feature_switch_field.disabled = True
                                    feature_horizontal = Horizontal(
                                        feature_text,
                                        feature_switch_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{feature}",
                                    )
                                    if (
                                        feature in advanced_features
                                        or feature in accel_features
                                    ):
                                        feature_horizontal.display = False
                                    yield feature_horizontal

                        # Create button. Handled solely by its decorated function down below.
                        yield Button("[b]Create", id="send", disabled=True)

                    with VerticalScroll(classes="event-text"):
                        """Right column.
                        Used for active debug purposes by showing the Lua output or eventual warnings.
                        """
                        yield Static(self.featurecode, id="main-text", classes="text")

            # QUALITY TAB
            with TabPane("Quality Profiles", id="quality_tab") as quality_tab:
                quality_tab.disabled = True
                with Container(
                    classes="app-grid"
                ):  # Overall container. allows for agile widget placements.
                    # Here, it uses the 'grid' format spanning 3 columns and 1 row.
                    with VerticalScroll(
                        classes="features"
                    ):  # left side vertical column, containing the feature fields.

                        # Printer settings
                        yield Static(
                            "[b]Quality presets",
                            classes="label",
                            id="static_quality_presets",
                        )

                        yield Horizontal(
                            Static(
                                "Print quality",
                                classes="feature-text",
                                id="static_quality_level",
                            ),
                            # Input widgets define an input field.
                            # its "type" attribute allows for active input restriction (either "text", "number", or "integer")
                            # its value is stored in a "value" attribute,
                            # only accessible through private method "__getattribute__('value')" or 
                            #publicly through event controls (down below)
                            Select(
                                prompt="Print quality",
                                id="quality",
                                options=[
                                    ("low", "low"),
                                    ("medium", "medium"),
                                    ("high", "high"),
                                ],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        # Other parameters. loops through quality_features to create remaining input fields.
                        for category in quality_features:  # category is a key
                            tmp_key_words = [
                                word for word in category.split("_")
                            ]  # List of words in the feature's name.
                            # Used solely for proper text display purposes
                            placeholder_value = ""  # tmp variable used to concatenate the new title altogether.
                            for word in tmp_key_words:
                                placeholder_value += word + " "
                            title_tmp = Static(
                                f"[b]{placeholder_value.title()}",
                                classes="label",
                                id=f"static_{category}_pq",
                            )  # .title() built-in
                            # function uppercases each starting letter.
                            yield title_tmp

                            # Loops through each feature in a category
                            for feature in quality_features[
                                category
                            ]:  # feature is also a key.
                                tmp_feature_words = [
                                    word for word in feature.split("_")
                                ]
                                placeholder_value = ""
                                for word in tmp_feature_words:
                                    if word in ["mm", "c"] and feature.endswith(
                                        word
                                    ):  # temporary solution to decorate units.
                                        # Will find better later.
                                        placeholder_value += f"({word})"
                                    else:
                                        placeholder_value += word + " "
                                if not isinstance(
                                    quality_features[category][feature], bool
                                ):  # non bool- features will yield an Input widget,
                                    # while bools will yield a Switch
                                    feature_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{feature}_pq",
                                    )
                                    feature_input_field = Input(
                                        value=f"{quality_features[category][feature]}",
                                        placeholder=f"{placeholder_value}",
                                        id=f"{feature}_pq",
                                        type="number",
                                        max_length=5,
                                        valid_empty=False,
                                    )
                                    if feature in start_as_disabled:
                                        feature_input_field.disabled = True
                                    feature_horizontal = Horizontal(
                                        feature_text,
                                        feature_input_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{feature}_pq",
                                    )
                                    # if feature in advanced_features: #features judged too advanced for a beginner
                                    #     #are by default hidden
                                    #     feature_horizontal.display = False
                                    yield feature_horizontal

                                else:  # bool features'case
                                    feature_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{feature}_pq",
                                    )
                                    feature_switch_field = Switch(
                                        value=quality_features[category][feature],
                                        id=f"{feature}_pq",
                                        animate= False
                                    )
                                    if feature in start_as_disabled:
                                        feature_switch_field.disabled = True
                                    feature_horizontal = Horizontal(
                                        feature_text,
                                        feature_switch_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{feature}_pq",
                                    )
                                    # if feature in advanced_features:
                                    #     feature_horizontal.display = False
                                    yield feature_horizontal

                        # Create button. Handled solely by its decorated function down below.
                        yield Button("[b]Create", id="send-pq", disabled=False)

                    with VerticalScroll(classes="event-text"):
                        """Right column.
                        Used for active debug purposes by showing the Lua output or eventual warnings.
                        """
                        yield Static(
                            self.featurecode, id="main-text-pq", classes="text"
                        )

            # MATERIALS TAB
            with TabPane("Materials", id="materials_tab") as materials_tab:
                materials_tab.disabled = True
                with Container(
                    classes="app-grid"
                ):  # Overall container. allows for agile widget placements.
                    # Here, it uses the 'grid' format spanning 3 columns and 1 row.
                    with VerticalScroll(
                        classes="features"
                    ):  # left side vertical column, containing the feature fields.

                        # Printer settings
                        yield Static(
                            "[b]Materials override",
                            classes="label",
                            id="static_materials_override",
                        )

                        yield Horizontal(
                            Static(
                                "Material", classes="feature-text", id="static_material"
                            ),
                            # Input widgets define an input field.
                            # its "type" attribute allows for active input restriction (either "text", "number", or "integer")
                            # its value is stored in a "value" attribute,
                            # only accessible through private method "__getattribute__('value')" or publicly through event controls (down below)
                            Select(
                                prompt="Filament material",
                                id="material",
                                options=[
                                    ("PLA", "PLA"),
                                    ("ABS", "ABS"),
                                    ("PETG", "PETG"),
                                ],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        yield Static(
                            "[b]Extruder changes",
                            classes="label",
                            id="static_extruder_changes",
                        )
                        yield Horizontal(
                            Static(
                                "Nozzle Diameter (mm)",
                                classes="feature-text",
                                id="static_nozzle_diameter_mm_0_pm",
                            ),
                            Select(
                                value=0.4,
                                prompt="Nozzle diameter (mm)",
                                id="nozzle_diameter_mm_0_pm",
                                options=[("0.25", 0.25), ("0.4", 0.4), ("0.6", 0.6)],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        yield Horizontal(
                            Static(
                                f"Filament diameter",
                                classes="feature-text",
                                id="static_filament_diameter_mm_0_pm",
                            ),
                            Select(
                                prompt="filament diameter (mm)",
                                id="filament_diameter_mm_0_pm",
                                options=[("1.75", 1.75), ("2.85", 2.85)],
                                allow_blank=False,
                            ),
                            classes="horizontal-layout",
                        )

                        fil_adv_fact = Horizontal(
                            Static(
                                "Filament Linear Advance Factor",
                                classes="feature-text",
                                id="static_filament_linear_adv_factor_pm",
                            ),
                            Input(
                                value="0.06",
                                placeholder="filament linear advance factor",
                                id="filament_linear_adv_factor_pm",
                                type="number",
                                max_length=2,
                                valid_empty=False,
                            ),
                            classes="horizontal-layout",
                            id="horizontal_filament_linear_adv_factor_pm",
                        )

                        yield fil_adv_fact

                        # Other parameters. loops through materials_features to create remaining input fields.
                        for category in materials_features:  # category is a key
                            tmp_key_words = [
                                word for word in category.split("_")
                            ]  # List of words in the feature's name.
                            # Used solely for proper text display purposes
                            placeholder_value = ""  # tmp variable used to concatenate the new title altogether.
                            for word in tmp_key_words:
                                placeholder_value += word + " "
                            title_tmp = Static(
                                f"[b]{placeholder_value.title()}",
                                classes="label",
                                id=f"static_{category}_pm",
                            )  # .title() built-in
                            # function uppercases each starting letter.
                            yield title_tmp

                            # Loops through each feature in a category
                            for feature in materials_features[
                                category
                            ]:  # feature is also a key.
                                tmp_feature_words = [
                                    word for word in feature.split("_")
                                ]
                                placeholder_value = ""
                                for word in tmp_feature_words:
                                    if word in ["mm", "c"] and feature.endswith(
                                        word
                                    ):  # temporary solution to decorate units.
                                        # Will find better later.
                                        placeholder_value += f"({word})"
                                    else:
                                        placeholder_value += word + " "
                                if not isinstance(
                                    materials_features[category][feature], bool
                                ):  # non bool- features will yield an Input widget,
                                    # while bools will yield a Switch
                                    feature_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{feature}_pm",
                                    )
                                    feature_input_field = Input(
                                        value=f"{materials_features[category][feature]}",
                                        placeholder=f"{placeholder_value}",
                                        id=f"{feature}_pm",
                                        type="number",
                                        max_length=5,
                                        valid_empty=False,
                                    )
                                    if feature in start_as_disabled:
                                        feature_input_field.disabled = True
                                    feature_horizontal = Horizontal(
                                        feature_text,
                                        feature_input_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{feature}_pm",
                                    )
                                   
                                   
                                    yield feature_horizontal

                                else:  # bool features'case
                                    feature_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{feature}_pm",
                                    )
                                    feature_switch_field = Switch(
                                        value=materials_features[category][feature],
                                        id=f"{feature}_pm",
                                        animate= False
                                    )
                                    if feature in start_as_disabled:
                                        feature_switch_field.disabled = True
                                    feature_horizontal = Horizontal(
                                        feature_text,
                                        feature_switch_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{feature}_pm",
                                    )
                                    # if feature in advanced_features:
                                    #     feature_horizontal.display = False
                                    yield feature_horizontal

                        # Create button. Handled solely by its decorated function down below.
                        yield Button("[b]Create", id="send-pm", disabled=False)

                    with VerticalScroll(classes="event-text"):
                        """Right column.
                        Used for active debug purposes by showing the Lua output or eventual warnings.
                        """
                        yield Static(
                            self.featurecode, id="main-text-pm", classes="text"
                        )

            # PRINTER.LUA TAB
            with TabPane("G-code translation", id="gcode_tab") as gcode_tab:
                gcode_tab.disabled = False #gcode tab is always enabled

                with Container(classes="app-grid-2"):
                    #Next Static widget is a warning message to the user.
                    yield Static(
                        '''Code snippets are automatically generated according to parameters input in the Features tab. Please modify each function with extreme precaution as it will directly command your machine.''',
                            classes='warning')
                    
                    #Left side of the tab with default variables
                    with VerticalScroll(classes="features-2"):
                        yield Horizontal(
                            Static(
                                'Toggle code modification',
                                classes="feature-text",
                                id='static_toggle_code_modification',),
                            Switch(
                                False,
                                id='toggle_code_modification',
                                classes='important_toggle',
                                animate= False),
                            classes='horizontal-layout')

                    #Yielding variables from the main_variables dictionary to create input fields (except for path_type)    
                        for variable in main_variables:
                            if variable != "path_type":
                                tmp_variable_words = [
                                    word for word in variable.split("_")
                                ]
                                placeholder_value = ""
                                for word in tmp_variable_words:
                                    placeholder_value += word + " "
                                if not isinstance(
                                    main_variables[variable], bool
                                ):  # non bool- variables will yield an Input widget,
                                    # while bools will yield a Switch
                                    variable_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{variable}",
                                    )
                                    variable_input_field = Input(
                                        value=f"{main_variables[variable]}",
                                        placeholder=f"{placeholder_value}",
                                        id=f"{variable}",
                                        type="number",
                                        max_length=5,
                                        valid_empty=False,
                                    )
                                    variable_horizontal = Horizontal(
                                        variable_text,
                                        variable_input_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{variable}",
                                    )
                                    # if feature in advanced_features: #features judged too advanced for a beginner
                                    #     #are by default hidden
                                    # feature_horizontal.display = False
                                    yield variable_horizontal
                                else:  # bool features'case
                                    variable_text = Static(
                                        f"{placeholder_value}",
                                        classes="feature-text",
                                        id=f"static_{variable}",
                                    )
                                    variable_switch_field = Switch(
                                        value=main_variables[variable], id=f"{variable}", animate= False
                                    )
                                    variable_horizontal = Horizontal(
                                        variable_text,
                                        variable_switch_field,
                                        classes="horizontal-layout",
                                        id=f"horizontal_{variable}",
                                    )
                                    # if feature in advanced_features:
                                    #     feature_horizontal.display = False
                                    yield variable_horizontal
                        
                        yield Button("[b]Create", id="send-printer", disabled=True)

                    #Right side of the tab with the printer.lua code editor
                    with VerticalScroll(classes="event-text-2", disabled=True, id='event-text-2'):
                        header_static = Static(
                            f"Header", classes="label", id=f"static_header"
                        )
                        #TextArea widget is used to create a code editor. It is a multi-line input field.
                        #Its highlighter is defined by the "language" attribute using Tree-sitter. 
                        # #Set to "python" because the Lua one is deprecated.
                        header_area = TextArea.code_editor(
                            self.header,
                            classes="features",
                            language="python",
                            id="header",
                        )
                        yield header_static
                        yield header_area

                        footer_static = Static(
                            f"Footer", classes="label", id=f"static_footer"
                        )
                        footer_area = TextArea.code_editor(
                            text=self.footer,
                            classes="features",
                            language="python",
                            id="footer",
                        )
                        yield footer_static
                        yield footer_area

                        #Yielding the functions from the function_dict dictionary to create code editor fields.
                        for category in self.function_dict:
                            for function in self.function_dict[category]:
                                function_static = Static(
                                    f"{function.title()}",
                                    classes="label",
                                    id=f"static_{function}",
                                )
                                function_area = TextArea.code_editor(
                                    self.function_dict[category][function],
                                    classes="features",
                                    language="python",
                                    id=f"{function}",
                                )
                                yield function_static
                                yield function_area

    @on(Switch.Changed)  # decorator called upon receiving a change in one of the yielded Switch widgets.
    # this decorator declares the following method as a message handler.
    def on_switch_changed(self, event: Switch.Changed) -> None:  # the event class gets the switch's id, value, and more.
        """
        Handles the switch widgets' events.
        """

        if (
            event.switch.id == "add_brim"
        ):  # since "add_brim" is a Switch, its "value" attribute can only be a bool
            if (
                event.switch.value == False
            ):  # if "add brim" is disabled, dependant features will be disabled and
                # output as comments in the lua file (see output handler below).

                self.query("#brim_distance_to_print_mm").first().disabled = (
                    True  # the query('#widget_id') method summons a widget
                )
                # thanks to its id, giving us access to its methods and attributes.
                self.query("#brim_num_contours").first().disabled = True

            else:  # otherwise, toggle them back on and output their values correctly in the lua file.
                self.query("#brim_distance_to_print_mm").first().disabled = False
                self.query("#brim_num_contours").first().disabled = False

        if event.switch.id == "enable_z_lift":  # ditto
            if event.switch.value == False:
                self.query("#extruder_swap_zlift_mm").first().disabled = True
                self.query("#z_lift_mm").first().disabled = True
            else:
                self.query("#z_lift_mm").first().disabled = False
                self.query("#z_lift_mm").first().disabled = False

        if (
            event.switch.id == "enable_acceleration"
        ):  # displays/hides acceleration-related features in advanced mode,
            # and most importantly, entirely disables/enables its handling.
            self.enable_acceleration = event.value
            self.refresh_header()
            self.refresh_footer()

            if event.switch.value == False:
                for feature in accel_features:
                    self.query(f"#{feature}").first().disabled = True
                    self.query(f"#horizontal_{feature}").first().display = False
            else:
                for feature in accel_features:
                    if feature not in ["default_jerk", "infill_jerk"]:
                        self.query(f"#{feature}").first().disabled = False
                    self.query(f"#horizontal_{feature}").first().display = True

        if event.switch.id == "auto_bed_leveling":
            self.auto_bed_leveling = event.value
            self.query('#reload_bed_mesh').first().disabled = not event.value
            self.refresh_header()

        if event.switch.id == "reload_bed_mesh":
            self.reload_bed_mesh = event.value
            self.refresh_header()

        if event.switch.id == 'use_per_path_accel':
            self.use_per_path_accel = event.value
            self.refresh_move_xyz()
            self.refresh_move_xyze()

        if event.switch.id == 'craftware_debug':
            self.craftware_debug = event.value
            self.refresh_move_xyze()

        if (event.switch.id == "advanced_mode"):# toggles advanced mode and displays hidden feature fields.
            if event.switch.value == False:
                self.query(f"#horizontal_enable_acceleration").first().display = False
                for feature in advanced_features:
                    self.query(f"#horizontal_{feature}").first().display = False
            else:
                self.query(f"#horizontal_enable_acceleration").first().display = True
                for feature in advanced_features:
                    self.query(f"#horizontal_{feature}").first().display = True

        if event.switch.id == "heated_chamber":
            self.heated_chamber = event.value
            self.refresh_header()
            if event.value:
                self.query("#chamber_temp_degree_c").first().disabled = False
                self.query("#chamber_temp_degree_c_min").first().disabled = False
                self.query("#chamber_temp_degree_c_max").first().disabled = False
                self.query("#chamber_temp_degree_c_pm").first().disabled = False
            else:
                self.query("#chamber_temp_degree_c").first().disabled = True
                self.query("#chamber_temp_degree_c_min").first().disabled = True
                self.query("#chamber_temp_degree_c_max").first().disabled = True
                self.query("#chamber_temp_degree_c_pm").first().disabled = True

        if event.switch.id == "enable_fan_pm":
            if event.value:
                self.query("#fan_speed_percent_pm").first().disabled = False
                self.query("#fan_speed_percent_on_bridges_pm").first().disabled = False
            else:
                self.query("#fan_speed_percent_pm").first().disabled = True
                self.query("#fan_speed_percent_on_bridges_pm").first().disabled = True

        if event.switch.id == "classic_jerk":
            self.classic_jerk = event.value
            if event.value:
                self.query("#default_jerk").first().disabled = False
                self.query("#infill_jerk").first().disabled = False

                self.query("#default_junction_deviation").first().disabled = True
                self.query("#perimeter_junction_deviation").first().disabled = True
                self.query("#infill_junction_deviation").first().disabled = True
                self.query("#travel_junction_deviation").first().disabled = True
            else:
                self.query("#default_jerk").first().disabled = True
                self.query("#infill_jerk").first().disabled = True

                self.query("#default_junction_deviation").first().disabled = False
                self.query("#perimeter_junction_deviation").first().disabled = False
                self.query("#infill_junction_deviation").first().disabled = False
                self.query("#travel_junction_deviation").first().disabled = False

        if event.switch.id == 'toggle_code_modification':
            if event.value:
                self.query('#event-text-2').first().disabled = False
            else:
                self.query('#event-text-2').first().disabled = True
    @on(Select.Changed)  # handles the case of Select widgets being modified.
    def on_select_changed(self, event: Select.Changed) -> None:
        """
        Handles the select widgets' events.
        """

        if (
            event.select.id == "extruder_count"
        ):  # loops through all hidden features describing additional extruders to display/hide them.
            # hidden extruder settings will not be written in the lua output at all, for clarity purposes.
            for extruder in range(
                1, event.select.value
            ):  # displays the correct amount of extruders
                self.query(f"#horizontal_nozzle_{extruder}").first().display = True
                self.query(f"#horizontal_fildiam_{extruder}").first().display = True

            for extruder in range(event.select.value, 14):  # hides the rest
                self.query(f"#horizontal_nozzle_{extruder}").first().display = False
                self.query(f"#horizontal_fildiam_{extruder}").first().display = False

            self.extruder_count = (
                event.select.value
            )  # we store the number of extruders in a reactive variable
            self.refresh_select_extruder()
            # as it will be used for the final output.
            if event.value > 1:
                self.query("#extruder_swap_zlift_mm").first().disabled = False
                self.query("#extruder_swap_retract_length_mm").first().disabled = False
                self.query(
                    "#extruder_swap_retract_speed_mm_per_sec"
                ).first().disabled = False
            else:
                self.query("#extruder_swap_zlift_mm").first().disabled = True
                self.query("#extruder_swap_retract_length_mm").first().disabled = True
                self.query(
                    "#extruder_swap_retract_speed_mm_per_sec"
                ).first().disabled = True
        if event.select.id == "bed_circular":  # handles the bed shape.
            # A circular bed (value= True) enables the display of "bed_radius" and deactivates the ability to modify x and y bd sizes
            # as they are defined as 2* the bed_radius
            if event.select.value == False:
                self.query("#bed_radius").first().disabled = True
                self.query("#horizontal_bed_radius").first().display = False

                self.query("#bed_size_x_mm").first().disabled = False
                self.query("#bed_size_y_mm").first().disabled = False
            else:
                self.query("#bed_radius").first().disabled = False
                self.query("#horizontal_bed_radius").first().display = True

                new_radius = float(
                    self.query("#bed_radius").first().__getattribute__("value")
                )
                self.query("#bed_size_x_mm").first().__setattr__(
                    "value", f"{new_radius*2}"
                )
                self.query("#bed_size_y_mm").first().__setattr__(
                    "value", f"{new_radius*2}"
                )

                self.query("#bed_size_x_mm").first().disabled = True
                self.query("#bed_size_y_mm").first().disabled = True

        if event.select.id in [f"nozzle_diameter_mm_{i}" for i in range(self.extruder_count)]:  # minimum and maximum layer thicknesses
            # are rescaled values of the nozzle_diameter.
            values = [self.query(f"#nozzle_diameter_mm_{i}").first().__getattribute__("value")
                for i in range(self.extruder_count)]
            
            min_nozzle_diam = min(values)
            max_nozzle_diam = max(values)

            self.query("#z_layer_height_mm_min").first().__setattr__(
                "value", f"{round(min_nozzle_diam*0.1, 2)}"
            )
            self.query("#z_layer_height_mm_max").first().__setattr__(
                "value", f"{round(max_nozzle_diam*0.9, 2)}"
            )
        
        if event.select.id == 'nozzle_diameter_mm_0':
            self.nozzle_diameter = event.value
            self.query('#volumetric_flow').first().__setattr__(
                    'value', f"{round(float(event.value)*float(self.layer_height)*float(self.printing_speed), 2)}")

        # firmware selection drastically modifies the generated lua code.
        if event.select.id == "firmware":
            self.firmware = event.value
            if event.value == 0:
                self.function_dict = marlin_function_dict
                self.header_dict = marlin_header_dict
                self.footer_dict = marlin_footer_dict
                self.select_extruder_dict= marlin_select_extruder_dict
                self.move_xyz_dict = marlin_move_xyz_dict
                self.move_xyze_dict = marlin_move_xyze_dict
                
            elif event.value == 1:
                self.function_dict = rrf_function_dict
                self.header_dict = rrf_header_dict
                self.footer_dict = rrf_footer_dict
                self.select_extruder_dict= rrf_select_extruder_dict
                self.move_xyz_dict = rrf_move_xyz_dict
                self.move_xyze_dict = rrf_move_xyze_dict
            else:
                self.function_dict = klipper_function_dict
                self.header_dict = klipper_header_dict
                self.footer_dict = klipper_footer_dict
                self.select_extruder_dict= klipper_select_extruder_dict
                self.move_xyz_dict = klipper_move_xyz_dict
                self.move_xyze_dict = klipper_move_xyze_dict

            #other firmwares have different handling of acceleration and jerk settings.
            if (event.value != 0): # if not Marlin
                self.query("#classic_jerk").first().__setattr__("value", True)
                self.query("#classic_jerk").first().disabled = True
                self.query("#default_jerk").first().disabled = False
                self.query("#infill_jerk").first().disabled = False
                self.query("#default_junction_deviation").first().disabled = True
                self.query("#perimeter_junction_deviation").first().disabled = True
                self.query("#infill_junction_deviation").first().disabled = True
                self.query("#travel_junction_deviation").first().disabled = True
            else:
                self.query("#classic_jerk").first().__setattr__("value", False)
                self.query("#classic_jerk").first().disabled = False
                self.query("#default_junction_deviation").first().disabled = False
                self.query("#perimeter_junction_deviation").first().disabled = False
                self.query("#infill_junction_deviation").first().disabled = False
                self.query("#travel_junction_deviation").first().disabled = False

            self.refresh_header()
            self.refresh_footer()
            self.refresh_move_xyz()
            self.refresh_move_xyze()
            self.refresh_select_extruder()

        # default quality values
        if event.select.id == "quality":
            self.quality = event.value
            if event.value == "low":
                self.query("#z_layer_height_mm_pq").first().__setattr__(
                    "value", str(0.2)
                )
                self.query("#priming_mm_per_sec_pq").first().__setattr__(
                    "value", str(30)
                )
                self.query("#print_speed_mm_per_sec_pq").first().__setattr__(
                    "value", str(60)
                )
                self.query("#cover_print_speed_mm_per_sec_pq").first().__setattr__(
                    "value", str(35)
                )

            if event.value == "medium":
                self.query("#z_layer_height_mm_pq").first().__setattr__(
                    "value", str(0.15)
                )
                self.query("#priming_mm_per_sec_pq").first().__setattr__(
                    "value", str(40)
                )
                self.query("#print_speed_mm_per_sec_pq").first().__setattr__(
                    "value", str(40)
                )
                self.query("#cover_print_speed_mm_per_sec_pq").first().__setattr__(
                    "value", str(25)
                )

            if event.value == "high":
                self.query("#z_layer_height_mm_pq").first().__setattr__(
                    "value", str(0.1)
                )
                self.query("#priming_mm_per_sec_pq").first().__setattr__(
                    "value", str(50)
                )
                self.query("#print_speed_mm_per_sec_pq").first().__setattr__(
                    "value", str(50)
                )
                self.query("#cover_print_speed_mm_per_sec_pq").first().__setattr__(
                    "value", str(30)
                )

        if event.select.id == "material":
            self.material = event.value
            if event.value == "PLA":
                self.query("#nozzle_diameter_mm_0_pm").first().__setattr__("value", 0.4)
                self.query("#filament_diameter_mm_0_pm").first().__setattr__(
                    "value", 1.75
                )
                self.query("#filament_linear_adv_factor_pm").first().__setattr__(
                    "value", str(0.06)
                )
                self.query("#filament_priming_mm_pm").first().__setattr__(
                    "value", str(45)
                )
                self.query("#extruder_temp_degree_c_pm").first().__setattr__(
                    "value", str(210)
                )
                self.query("#bed_temp_degree_c_pm").first().__setattr__(
                    "value", str(60)
                )
                self.query("#fan_speed_percent_pm").first().__setattr__(
                    "value", str(100)
                )
                self.query("#fan_speed_percent_on_bridges_pm").first().__setattr__(
                    "value", str(100)
                )
                self.query("#print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(60)
                )
                self.query("#perimeter_print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(45)
                )
                self.query("#cover_print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(30)
                )
                self.query(
                    "#first_layer_print_speed_mm_per_sec_pm"
                ).first().__setattr__("value", str(20))

            if event.value == "ABS":
                self.query("#nozzle_diameter_mm_0_pm").first().__setattr__("value", 0.6)
                self.query("#filament_diameter_mm_0_pm").first().__setattr__(
                    "value", 1.75
                )
                self.query("#filament_linear_adv_factor_pm").first().__setattr__(
                    "value", str(0.04)
                )
                self.query("#filament_priming_mm_pm").first().__setattr__(
                    "value", str(45)
                )
                self.query("#extruder_temp_degree_c_pm").first().__setattr__(
                    "value", str(240)
                )
                self.query("#bed_temp_degree_c_pm").first().__setattr__(
                    "value", str(100)
                )
                self.query("#enable_fan_pm").first().__setattr__("value", False)
                self.query("#fan_speed_percent_pm").first().__setattr__(
                    "value", str(100)
                )
                self.query("#fan_speed_percent_on_bridges_pm").first().__setattr__(
                    "value", str(100)
                )
                self.query("#print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(50)
                )
                self.query("#perimeter_print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(45)
                )
                self.query("#cover_print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(45)
                )
                self.query(
                    "#first_layer_print_speed_mm_per_sec_pm"
                ).first().__setattr__("value", str(20))

            if event.value == "PETG":
                self.query("#nozzle_diameter_mm_0_pm").first().__setattr__("value", 0.6)
                self.query("#filament_diameter_mm_0_pm").first().__setattr__(
                    "value", 1.75
                )
                self.query("#filament_linear_adv_factor_pm").first().__setattr__(
                    "value", str(0.08)
                )
                self.query("#extruder_temp_degree_c_pm").first().__setattr__(
                    "value", str(230)
                )
                self.query("#bed_temp_degree_c_pm").first().__setattr__(
                    "value", str(75)
                )
                self.query("#enable_fan_pm").first().__setattr__("value", True)
                self.query("#fan_speed_percent_pm").first().__setattr__(
                    "value", str(45)
                )
                self.query("#fan_speed_percent_on_bridges_pm").first().__setattr__(
                    "value", str(75)
                )
                self.query("#print_speed_mm_per_sec").first().__setattr__(
                    "value", str(120)
                )
                self.query("#perimeter_print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(80)
                )
                self.query("#cover_print_speed_mm_per_sec_pm").first().__setattr__(
                    "value", str(80)
                )
                self.query(
                    "#first_layer_print_speed_mm_per_sec_pm"
                ).first().__setattr__("value", str(30))
    
    @on(Input.Changed)  # handles the case of input widgets being modified.
    def on_input_changed(self, event: Input.Changed) -> None:
        """
        Handles the input widgets' events.
        """

        if event.input.id == "name":
            self.name = event.value

            if event.validation_result.is_valid == False:
                # error log
                self.featurecode = ""
                for error in event.validation_result.failure_descriptions:
                    self.featurecode += error + "\n"
                self.featurecode += "\nName needed to activate other tabs."
                self.query_one("#main-text").update(self.featurecode)

                # disables the other tabs
                self.query("#quality_tab").first().disabled = True
                self.query("#materials_tab").first().disabled = True
                self.query("#send").first().disabled = True
                self.query("#send-printer").first().disabled = True
            else:
                self.featurecode = ""
                self.query_one("#main-text").update(self.featurecode)
                self.query_one("#main-text-pq").update(self.featurecode)
                self.query_one("#main-text-pm").update(self.featurecode)

                self.query("#quality_tab").first().disabled = False
                self.query("#materials_tab").first().disabled = False
                self.query("#send").first().disabled = False
                self.query("#send-printer").first().disabled = False

        if event.input.id == "bed_radius":  # auto rescaling of the bed size values.
            if event.value != "":
                self.query("#bed_size_x_mm").first().__setattr__(
                    "value", f"{float(event.value)*2}"
                )
                self.query("#bed_size_y_mm").first().__setattr__(
                    "value", f"{float(event.value)*2}"
                )

        if event.input.id == "print_speed_mm_per_sec":
            self.printing_speed = event.value
            if event.value != "":
                self.query("#print_speed_mm_per_sec_min").first().__setattr__(
                    "value", f"{round(float(event.value)/3, 2)}"
                )
                self.query("#print_speed_mm_per_sec_max").first().__setattr__(
                    "value", f"{round(float(event.value)*3.5, 2)}"
                )

                self.query("#perimeter_print_speed_mm_per_sec").first().__setattr__(
                    "value", f"{round(float(event.value)*0.75, 2)}"
                )
                self.query("#perimeter_print_speed_mm_per_sec_min").first().__setattr__(
                    "value", f"{round(float(event.value)/3, 2)}"
                )
                self.query("#perimeter_print_speed_mm_per_sec_max").first().__setattr__(
                    "value", f"{round(float(event.value)*2.8, 2)}"
                )

                self.query("#cover_print_speed_mm_per_sec").first().__setattr__(
                    "value", f"{round(float(event.value)*0.75, 2)}"
                )
                self.query("#cover_print_speed_mm_per_sec_min").first().__setattr__(
                    "value", f"{round(float(event.value)/3, 2)}"
                )
                self.query("#cover_print_speed_mm_per_sec_max").first().__setattr__(
                    "value", f"{round(float(event.value)*2.8, 2)}"
                )

                self.query("#first_layer_print_speed_mm_per_sec").first().__setattr__(
                    "value", f"{round(float(event.value)/3, 2)}"
                )
                self.query(
                    "#first_layer_print_speed_mm_per_sec_max"
                ).first().__setattr__("value", f"{round(float(event.value)*2.8, 2)}")

                self.query("#travel_speed_mm_per_sec").first().__setattr__(
                    "value", f"{round(float(event.value)*3, 2)}"
                )
                self.query('#volumetric_flow').first().__setattr__(
                    'value', f"{round(float(event.value)*float(self.nozzle_diameter)*float(self.layer_height) ,2)}")

        if event.input.id == 'z_layer_height_mm':
            self.layer_height = event.value
            self.query('#volumetric_flow').first().__setattr__(
                    'value', f"{round(float(event.value)*float(self.nozzle_diameter)*float(self.printing_speed), 2)}")

        if event.input.id == "default_acc":
            if event.value != "":
                self.query("#e_prime_max_acc").first().__setattr__(
                    "value", f"{round(float(event.value)/2)}"
                )
                self.query("#perimeter_acc").first().__setattr__(
                    "value", f"{round(float(event.value)/2)}"
                )
                self.query("#infill_acc").first().__setattr__(
                    "value", f"{round(float(event.value))}"
                )
                self.query("#x_max_acc").first().__setattr__(
                    "value", f"{round(float(event.value))}"
                )
                self.query("#y_max_acc").first().__setattr__(
                    "value", f"{round(float(event.value))}"
                )
                self.query("#z_max_acc").first().__setattr__(
                    "value", f"{round(float(event.value)/40)}"
                )
                self.query("#e_max_acc").first().__setattr__(
                    "value", f"{round(float(event.value))}"
                )

        if event.input.id == "default_jerk":
            if event.value != "":
                self.query("#infill_jerk").first().__setattr__("value", event.value)

                default_accel = float(
                    self.query("#default_acc").first().__getattribute__("value")
                )
                perim_accel = float(
                    self.query("#perimeter_acc").first().__getattribute__("value")
                )
                infill_accel = float(
                    self.query("#infill_acc").first().__getattribute__("value")
                )
                self.query("#default_junction_deviation").first().__setattr__(
                    "value",
                    str(round(0.4 * (float(event.value) ** 2 / default_accel), 4)),
                )
                self.query("#perimeter_junction_deviation").first().__setattr__(
                    "value",
                    str(round(0.4 * (float(event.value) ** 2 / perim_accel), 4)),
                )
                self.query("#infill_junction_deviation").first().__setattr__(
                    "value",
                    str(round(0.4 * (float(event.value) ** 2 / infill_accel), 4)),
                )
                self.query("#travel_junction_deviation").first().__setattr__(
                    "value",
                    str(round(0.4 * (float(event.value) ** 2 / default_accel), 4)),
                )

    @on(TextArea.Changed)
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """
        Handles the text area widgets' events.
        """
        self.__dict__[event.text_area.id] = event.text_area.text

###Output handler

    @on(Button.Pressed)  # handles the case of the "create" button being pressed.
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles the button widgets' events.
        Specifically the "create" button and how it outputs the lua code.
        """

        #Features tab output
        if event.button.id == "send":
            errorsend = ""
            self.featurecode = ""  # empties the output.
            try:  # a try and catch section to raise errors when faulty lua outputs are made, i.e. empty values
                if self.name == "":
                    errorsend = "Missing value."
                    raise "Missing Value"
                self.featurecode += "--Custom profile for " + self.name + "\n"
                self.featurecode += (
                    "--Created on " + datetime.now().strftime("%x") + "\n \n"
                )

                self.featurecode += (
                    "--Firmware: 0 = Marlin; 1 = RRF; 2 = Klipper;\n"
                )
                self.featurecode += (
                    "firmware = "
                    + f'{self.query("#firmware").first().__getattribute__("value")}'
                )

                
                self.featurecode += (
                    "--Additional features: \n"
                )  # puts a commented title for clarity purposes
                self.featurecode += (
                    "add_checkbox_setting('auto_bed_leveling', 'Auto Bed Leveling','Use G29 Auto Leveling if the machine is equipped with one (BLTouch, Pinda, capacitive sensor, etc.)')\n"
                )
                self.featurecode += (
                    "add_checkbox_setting(reload_bed_mesh', 'Reload the last bed-mesh','Reload the last saved bed-mesh if available)\n"
                )
                self.featurecode += (
                    "add_checkbox_setting('use_per_path_accel', 'Uses Per-Path Acceleration', 'Manage Accelerations depending of the current path type')\n"
                )
                self.featurecode += (
                    "add_setting('volumetric_flow', 'Volumetric Flow', 0, 20, 'Product of printing speed, layer height and nozzle diameter', 4.8)\n \n"
                )


                for category in default_features:
                    errorsend = "category."
                    self.featurecode += (
                        "\n \n" + f"--{category}"
                    )  # puts said category as a commented title. solely for clarity purposes.
                    for feature in default_features[category]:
                        errorsend = "feature."
                        feature_value = str(
                            self.query(f"#{feature}").first().__getattribute__("value")
                        )  # use of the private "__getattribute__"
                        # method to query the field's value.
                        errorsend = "query_value."
                        if self.query(
                            f"#{feature}"
                        ).first().disabled == False or feature in [
                            "bed_size_x_mm",
                            "bed_size_y_mm",
                        ]:
                            # only enabled features are output normally, except for bed sizes as they are only deactivated
                            # in case of a circular bed.
                            if feature_value == "":  # avoids empty fields.
                                errorsend = "missing value 2."
                                raise "Missing Value"
                            else:  # due to laziness, every feature_value is lowercased so that specifically bool values get lowercased,
                                # thanks to lua's odd syntax.
                                errorsend = "lowercased."
                                self.featurecode += (
                                    "\n" + f"{feature} = " + feature_value.lower()
                                )
                                self.query("#main-text").first().update(
                                    f"{self.featurecode}"
                                )
                                errorsend = "query update 1."
                        else:  # disabled features are output as lua comments.
                            errorsend = "disabled."
                            self.featurecode += (
                                "\n" + f"--{feature} = " + feature_value.lower()
                            )
                            self.query("#main-text").first().update(
                                f"{self.featurecode}"
                            )
                            errorsend = "query update 2."

                for extruder in range(
                    1, int(self.extruder_count)
                ):  # handles similar actions for every additonal extruder settings.
                    # If no additional extruder, no additional comments shall be written.
                    errorsend = "extruders."
                    nozzle_value = str(
                        self.query(f"#nozzle_diameter_mm_{extruder}")
                        .first()
                        .__getattribute__("value")
                    )
                    errorsend = "extruders query 1."
                    self.featurecode += (
                        "\n" + f"nozzle_diameter_mm_{extruder} = " + nozzle_value
                    )
                    fildiam_value = str(
                        self.query(f"#filament_diameter_mm_{extruder}")
                        .first()
                        .__getattribute__("value")
                    )
                    errorsend = "extruders query 2."
                    self.featurecode += (
                        "\n" + f"filament_diameter_mm_{extruder} = " + fildiam_value
                    )
                    self.query("#main-text").first().update(f"{self.featurecode}")
                    errorsend = "extruders query 3."

                for (
                    category
                ) in features_dict:  # handles similar action for remaining features.
                    errorsend = "category 2."
                    self.featurecode += "\n \n" + f"--{category}"
                    for feature in features_dict[category]:
                        errorsend = "features 2."
                        feature_value = str(
                            self.query(f"#{feature}").first().__getattribute__("value")
                        )
                        errorsend = "query value 2."
                        if self.query(f"#{feature}").first().disabled == False:
                            if feature_value == "":
                                errorsend = "missing value 2."
                                raise "Missing Value"
                            else:
                                errorsend = "lowercased 2."
                                self.featurecode += (
                                    "\n" + f"{feature} = " + feature_value.lower()
                                )
                                self.query("#main-text").first().update(
                                    f"{self.featurecode}"
                                )
                                errorsend = "query update 3."
                        else:
                            errorsend = "disabled 2."
                            self.featurecode += (
                                "\n" + f"--{feature} = " + feature_value.lower()
                            )
                            self.query("#main-text").first().update(
                                f"{self.featurecode}"
                            )
                            errorsend = "query update 4."

                ## Folder creation (if it does not exist yet) and lua file dumping.
                name_words = self.name.split(" ")
                name = ""
                for word in name_words:
                    if word != name_words[-1]:
                        name += word + "_"
                    else:
                        name += word

                if f"{name}" not in os.listdir():
                    os.makedirs(f"{name}")
                dump_file = open(f"./{name}/features.lua", "w")
                dump_file.write(self.featurecode)
                self.copy_to_clipboard(self.featurecode)
                self.query("#gcode_tab").first().disabled = False
            except:  # if not successful, displays the following in the right panel.
                self.featurecode = (
                    errorsend + "\nPlease fill any empty information field(s)."
                )
                self.query("#main-text").first().update(f"{self.featurecode}")

        #Quality tab output
        if event.button.id == "send-pq":
            errorsend = ""
            self.featurecode = ""  # empties the output.
            try:  # a try and catch section to raise errors when faulty lua outputs are made, i.e. empty values
                if self.quality == "":
                    errorsend = "Missing value."
                    raise "Missing Value"
                self.featurecode += (
                    "--Custom quality profile: " + self.quality + f" for {self.name} \n"
                )
                self.featurecode += (
                    "--Created on " + datetime.now().strftime("%x") + "\n \n"
                )

                for category in quality_features:
                    errorsend = "category."
                    self.featurecode += (
                        "\n \n" + f"--{category}"
                    )  # puts said category as a commented title. solely for clarity purposes.
                    for feature in quality_features[category]:
                        errorsend = "feature."
                        feature_value = str(
                            self.query(f"#{feature}_pq")
                            .first()
                            .__getattribute__("value")
                        )  # use of the private "__getattribute__"
                        # method to query the field's value.
                        errorsend = "query_value."
                        if self.query(f"#{feature}_pq").first().disabled == False:
                            # only enabled features are output normally, except for bed sizes as they are only deactivated
                            # in case of a circular bed.
                            if feature_value == "":  # avoids empty fields.
                                errorsend = "missing value 2."
                                raise "Missing Value"
                            else:  # due to laziness, every feature_value is lowercased so that specifically bool values get lowercased,
                                # thanks to lua's odd syntax.
                                errorsend = "lowercased."
                                self.featurecode += (
                                    "\n" + f"{feature} = " + feature_value.lower()
                                )
                                self.query("#main-text-pq").first().update(
                                    f"{self.featurecode}"
                                )
                                errorsend = "query update 1."
                        else:  # disabled features are output as lua comments.
                            errorsend = "disabled."
                            self.featurecode += (
                                "\n" + f"--{feature} = " + feature_value.lower()
                            )
                            self.query("#main-text-pq").first().update(
                                f"{self.featurecode}"
                            )
                            errorsend = "query update 2."

                ## Folder creation (if it does not exist yet) and lua file dumping.
                quality_name_words = self.quality.split(" ")
                quality_name = ""
                for word in quality_name_words:
                    if word != quality_name_words[-1]:
                        quality_name += word + "_"
                    else:
                        quality_name += word

                if f"{self.name}" not in os.listdir() or f"{self.name}/profiles" not in os.listdir():
                    os.makedirs(f"{self.name}/profiles")
                dump_file = open(f"./{self.name}/profiles/{self.quality}.lua", "w")
                dump_file.write(self.featurecode)
                self.copy_to_clipboard(self.featurecode)

            except:  # if not successful, displays the following in the right panel.
                self.featurecode = (
                    errorsend + "\nPlease fill any empty information field(s)."
                )
                self.query("#main-text-pq").first().update(f"{self.featurecode}")

        #Materials tab output
        if event.button.id == "send-pm":
            errorsend = ""
            self.featurecode = ""  # empties the output.
            try:  # a try and catch section to raise errors when faulty lua outputs are made, i.e. empty values
                if self.quality == "":
                    errorsend = "Missing value."
                    raise "Missing Value"
                self.featurecode += (
                    "--Custom material profile: "
                    + self.material
                    + f" for {self.name} \n"
                )
                self.featurecode += (
                    "--Created on " + datetime.now().strftime("%x") + "\n \n"
                )

                self.featurecode += "\n \n" + "--extruder_changes"
                errorsend = "nu"
                self.featurecode += (
                    "\n"
                    + "nozzle_diameter_mm_0 = "
                    + f'{self.query("#nozzle_diameter_mm_0_pm").first().__getattribute__("value")}'
                )
                errorsend = "nus"
                self.featurecode += (
                    "\n"
                    + "filament_diameter_mm_0 = "
                    + f'{self.query("#filament_diameter_mm_0_pm").first().__getattribute__("value")}'
                )
                errorsend = "nuq"
                self.featurecode += (
                    "\n"
                    + "filament_linear_adv_factor = "
                    + str(
                        self.query("#filament_linear_adv_factor_pm")
                        .first()
                        .__getattribute__("value")
                    )
                )

                for category in materials_features:
                    errorsend = "category."
                    self.featurecode += ("\n \n" + f"--{category}")  # puts said category as a commented title. solely for clarity purposes.
                    for feature in materials_features[category]:
                        errorsend = "feature."
                        feature_value = str(
                            self.query(f"#{feature}_pm").first().__getattribute__("value")
                        )  # use of the private "__getattribute__"
                        # method to query the field's value.
                        errorsend = "query_value."
                        if self.query(f"#{feature}_pm").first().disabled == False:
                            # only enabled features are output normally, except for bed sizes as they are only deactivated
                            # in case of a circular bed.
                            if feature_value == "":  # avoids empty fields.
                                errorsend = "missing value 2."
                                raise "Missing Value"
                            else:  # due to laziness, every feature_value is lowercased so that specifically bool values get lowercased,
                                # thanks to lua's odd syntax.
                                errorsend = "lowercased."
                                self.featurecode += ("\n" + f"{feature} = " + feature_value.lower())
                                self.query("#main-text-pm").first().update(f"{self.featurecode}")
                                errorsend = "query update 1."
                        else:  # disabled features are output as lua comments.
                            errorsend = "disabled."
                            self.featurecode += ("\n" + f"--{feature} = " + feature_value.lower())
                            self.query("#main-text-pm").first().update(f"{self.featurecode}")
                            errorsend = "query update 2."

                ## Folder creation (if it does not exist yet) and lua file dumping.
                material_name_words = self.material.split(" ")
                material_name = ""
                for word in material_name_words:
                    if word != material_name_words[-1]:
                        material_name += word + "_"
                    else:
                        material_name += word

                if f"{self.name}" not in os.listdir() or f"{self.name}/materials" not in os.listdir():
                    os.makedirs(f"{self.name}/materials")
                dump_file = open(f"./{self.name}/materials/{self.material}.lua", "w")
                dump_file.write(self.featurecode)
                self.copy_to_clipboard(self.featurecode)

            except:  # if not successful, displays the following in the right panel.
                self.featurecode = (errorsend + "\nPlease fill any empty information field(s).")
                self.query("#main-text-pm").first().update(f"{self.featurecode}")


        #Printer tab output
        if event.button.id == "send-printer":
            errorsend = ""
            self.printercode = ""
            try:
                errorsend = "start"
                self.printercode += "--Printer functions for " + self.name + "\n"
                self.printercode += ("--Created on " + datetime.now().strftime("%x") + "\n \n")
                self.printercode += "--Firmware: 0 = Marlin; 1 = RRF; 2 = Klipper;\n"
                self.printercode += "firmware = " + f'{self.query("#firmware").first().__getattribute__("value")}' + "\n"
                self.printercode += ("output(';Layer height: ' .. round(z_layer_height_mm, 2)) \n")
                self.printercode += """output(';Generated with ' .. slicer_name .. ' ' .. slicer_version .. '\\n') \n \n"""
                self.printercode += "--//////////////////////////////////////////////////Defining main variables"

                for variable in main_variables:
                    errorsend = "var"
                    variable_value = str(self.query(f"#{variable}").first().__getattribute__("value"))  # use of the private "__getattribute__"
                    errorsend = "query var"
                    self.printercode += "\n" + f"{variable} = " + variable_value.lower()

                self.printercode += """

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

"""
                errorsend += "writing \n"
                self.printercode += "--//////////////////////////////////////////////////Main Functions - called by IceSL \n"
                self.printercode += "--################################################## HEADER & FOOTER \n"
                self.printercode += self.header
                self.printercode += "-----------------------"
                self.printercode += self.footer + "\n"

                errorsend += "did footer\n"
                for function_category in self.function_dict:
                    errorsend += "function category\n"
                    self.printercode += f"\n--################################################## {function_category}"
                    errorsend = "got to function dumping\n"
                    for function in self.function_dict[function_category]:
                        errorsend += f"one of your functions didn't get dumped {function}"
                        self.printercode += self.__getattribute__(function)
                        self.printercode += "-----------------------"

                self.printercode += '\n \n' + self.util_functions 

                ## Folder creation (if it does not exist yet) and lua file dumping.
                errorsend = "dumping"
                name_words = self.name.split(" ")
                name = ""
                for word in name_words:
                    if word != name_words[-1]:
                        name += word + "_"
                    else:
                        name += word

                    if f"{name}" not in os.listdir():
                        os.makedirs(f"{name}")
                    dump_file = open(f"./{name}/printer.lua", "w")
                    dump_file.write(self.printercode)
                    # self.copy_to_clipboard(self.printercode)
            except:
                # if not successful, displays the following log in the right panel.
                self.printercode = errorsend + "\nNOPE."
                self.query("#main-text").first().update(f"{self.printercode}")

###lua code refreshers
    def refresh_header(self) -> None:
        """
        function to refresh the header of the printer.lua file.
        """
        
        self.header = self.header_dict['start_header']

        if self.enable_acceleration:
            self.header += self.header_dict['enable_acceleration']
            if self.firmware == 0:
                if self.classic_jerk:
                    self.header += self.header_dict['jerk_true']
                else:
                    self.header += self.header_dict['jerk_false']

        self.header += self.header_dict['temp_setup']
        
        if self.heated_chamber:
            self.header += self.header_dict['heated_chamber']

        if self.firmware == 0:   
            self.header += self.header_dict['home_all']

        if self.auto_bed_leveling and not self.reload_bed_mesh:
            self.header += self.header_dict['auto_bed_leveling']

        elif self.auto_bed_leveling and self.reload_bed_mesh:
            self.header += self.header_dict['auto_bed_leveling_and_reload_bed_mesh']

        self.header += self.header_dict['end_header']

        self.query("#header").first().__setattr__("text", self.header)


    def refresh_footer(self) -> None:
        """
        function to refresh the footer of the printer.lua file.
        """

        self.footer = self.footer_dict['start_footer']

        if self.heated_chamber:
            self.footer += self.footer_dict['heated_chamber']

        if self.firmware == 0:
            self.footer += self.footer_dict['home_all']

        if self.enable_acceleration:
            self.footer += self.footer_dict['enable_acceleration']
            if self.firmware == 0:
                if self.classic_jerk:
                    self.footer += self.footer_dict['jerk_true']
                else:
                    self.footer += self.footer_dict['jerk_false']

        self.footer += self.footer_dict['end_footer']

        self.query("#footer").first().__setattr__("text", self.footer)


    def refresh_select_extruder(self) -> None:
        """
        function to refresh the select_extruder function of the printer.lua file.
        """

        self.select_extruder = self.select_extruder_dict['start_select_extruder']
        if self.extruder_count > 1:
            self.select_extruder += self.select_extruder_dict['multi_extruders']
        else:
            self.select_extruder += self.select_extruder_dict['solo_extruder']

        self.select_extruder += self.select_extruder_dict['end_select_extruder']

        self.query("#select_extruder").first().__setattr__("text", self.select_extruder)


    def refresh_move_xyz(self) -> None:
        """
        function to refresh the move_xyz function of the printer.lua file.
        """

        self.move_xyz = self.move_xyz_dict['start_move_xyz']

        if self.use_per_path_accel:
            self.move_xyz += self.move_xyz_dict['use_per_path_accel']

        self.move_xyz += self.move_xyz_dict['end_move_xyz']

        self.query("#move_xyz").first().__setattr__("text", self.move_xyz)


    def refresh_move_xyze(self) -> None:
        """
        function to refresh the move_xyze function of the printer.lua file.
        """

        self.move_xyze = self.move_xyze_dict['start_move_xyze']

        if self.craftware_debug:  
            self.move_xyze += self.move_xyze_dict['craftware_debug_true']
        else:
            self.move_xyze += self.move_xyze_dict['craftware_debug_false']

        self.move_xyze += self.move_xyze_dict['path_type']

        if self.use_per_path_accel:
            self.move_xyze += self.move_xyze_dict['use_per_path_accel']

        self.move_xyze += self.move_xyze_dict['end_move_xyze']

        self.query("#move_xyze").first().__setattr__("text", self.move_xyze)
    
    
    
    def on_mount(self) -> None:
        """
        Mounts the app.
        Adds the tooltips to the widgets.
        Initializes the header, footer, select_extruder, move_xyz and move_xyze.
        """

        self.screen.styles.background = "#E8E9F3"  # type: ignore

        # Tooltips:
        for key in tooltips:
            self.query(f"#{key}").first().tooltip = tooltips[key]

        self.refresh_header()
        self.refresh_footer()
        self.refresh_select_extruder()
        self.refresh_move_xyz()
        self.refresh_move_xyze()


def isNotSpaces(text: str):
    """
    Additional function to check if a text is not only spaces.
    """

    return not (text.strip() == "")


if __name__ == "__main__":
    app = gui()
    app.run()
