import asyncio
import os
import time
from yaml import load, Loader
import quart
from ..getdata import DataWrapper

class OwlRenderer:
    """
    Parser for owl config, renderer to HTML
    """

    def __init__(self, owl_config_path):
        """
        Parse provided owl config file into an OwlRenderer

        Arguments
        =========
        owl_config_path : str or File
            Path to the owl config file to load
        """
        self.owl_config_path = owl_config_path
        # TODO replace prints with proper logging
        print("Using owl configuration:", self.owl_config_path)

        with open(owl_config_path) as f:
            self.parsed_config = load(f, Loader=Loader)

        self.data_path = self.parsed_config["config"]["data_path"]
        if self.data_path == "FAKEFAKEFAKE":
            print("Using fake data")
            self.data_wrapper = DataWrapper(fake=True)
        else:
            print("Using data from", self.data_path)
            self.data_wrapper = DataWrapper(self.data_path)

        self.boxes = []
        for i, box in enumerate(self.parsed_config["layout"]):
            print("Adding box:", i, box)
            self.boxes.append(OwlBox(i, **box))

        self.all_entries = sum([b.entries for b in self.boxes], [])
        self.all_fields = list(set([e.field for e in self.all_entries]))
        print("All fields:" , self.all_fields)

    def _render_signals(self, data_values):
        """
        Render the formatted updates for all signals
        """
        signals = {}
        for entry in self.all_entries:
            value = entry.format_value(data_values[entry.field])
            signals[entry.signal_name] = value
        return signals

    async def wait_and_render_signal_updates(self):
        """
        Waits for new data and renders formatted signal updates
        """
        data_values = await self.data_wrapper.wait_for_new_data(self.all_fields)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._render_signals, data_values)

    async def render_template(self):
        """
        Render this object to its template.
        """
        # the signal update code can be used here to set the initial spec
        # populated with meaningful starting values
        # force data wrapper to load immediately without waiting for new values
        self.data_wrapper.last_index = None
        signals = await self.wait_and_render_signal_updates()
        self.signal_spec = str(signals)
        return await quart.render_template("owl/main.html", config=self)



class OwlBox:
    def __init__(self, num, name, entries, color="#333333", background_color="#eeeeee"):
        """
        Parse config for a box

        Arguments
        =========
        name : str
            The name of the box
        entries : list of dict
            The configuration for the entries (rows) in the box
        color : str or int, optional
            CSS color specification for the box title and border
        background_color : str or int, optional
            CSS color specification for the box background colour
        """
        self.num = num
        self.name = name
        self.entries = []
        for i, entry in enumerate(entries):
            print("Adding entry:", num, i, entry)
            self.entries.append(OwlEntry(num, i, **entry))
        self.color = color
        self.background_color = background_color

class OwlEntry:
    def __init__(self, box_num, num, label, field, format, limits=None):
        """
        Parse config for an entry from a dict of options

        Arguments
        =========
        label : str
            The entry label
        field : str
            The dirfile field from which to read the data
        format : str
            Formatting instructions
        limits : dict, optional
            Options for entry limits formatting
        """
        self.box_num = box_num
        self.num = num
        self.label = label
        self.field = field
        self.signal_name = f"field_{self.field}_b{box_num}_e{num}".lower()
        self.format = format
        if limits is not None:
            limit_type = limits["type"]
            if limit_type == "value_compare":
                self.limits = ValueCompareLimits(limits["comparisons"])
            else:
                raise ValueError(f"Unknown limit type: {limit_type}")

    def format_value(self, val):
        """
        Format a data value given this entry's format spec
        """
        format_type, format_str = self.format.split(":", 1)
        if format_type == "val":
            return ("{:" + format_str + "}").format(val)
        elif format_type == "time":
            return time.strftime(format_str, time.gmtime(val))

class ValueCompareLimits:
    def __init__(self, comparisons):
        """
        Parse config for value comparison styled limits

        Arguments
        =========
        comparisons : dict
            Limit specs. keys are CSS class names to display,
            and values are conditions under which to use that class.
        """
        self.comparisons = comparisons
