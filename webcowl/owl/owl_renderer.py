import asyncio
import copy
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
            print("Using fake owl data")
            self.data_wrapper = DataWrapper(fake=True)
        else:
            print("Using owl data from", self.data_path)
            self.data_wrapper = DataWrapper(self.data_path)

        self.boxes = []
        for i, box in enumerate(self.parsed_config["layout"]):
            self.boxes.append(OwlBox(i, **box))

        self.all_entries = sum([b.entries for b in self.boxes], [])
        self.all_fields = list(set([e.field for e in self.all_entries]))

    def clone(self):
        """
        Clone a copy of this object for use in separate requests
        """
        return copy.deepcopy(self)

    def _render_signals(self, data_values):
        """
        Render the formatted updates for all signals
        """
        signals = {}
        for entry in self.all_entries:
            value = entry.format_value(data_values[entry.field])
            signals[entry.signal_name] = value
        return signals

    async def wait_and_render_signal_updates(self, timeout=None):
        """
        Waits for new data and renders formatted signal updates
        """
        try:
            data_values = await asyncio.wait_for(self.data_wrapper.wait_for_new_data(self.all_fields), timeout=timeout)
            return await quart.utils.run_sync(self._render_signals)(data_values)
        except asyncio.TimeoutError:
            return {}

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
    def __init__(self, num, name, entries, width=1, color="#333333", background_color="#eeeeee"):
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
            self.entries.append(OwlEntry(num, i, **entry))
        self.width = f"{width*8}rem"
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
        self.limits = limits
        if self.limits is not None:
            limit_type = self.limits["type"]
            if limit_type == "value_compare":
                self.limits = ValueCompareLimits(self.signal_name, self.limits["comparisons"])
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

    def limits_attribute(self):
        """
        Output the limits as a datastar attribute
        """
        if self.limits is None:
            return ""
        else:
            return self.limits.to_attribute()

class ValueCompareLimits:
    def __init__(self, signal_name, comparisons):
        """
        Parse config for value comparison styled limits

        Arguments
        =========
        comparisons : dict
            Limit specs. keys are CSS class names to display,
            and values are conditions under which to use that class.
        """
        self.signal_name = signal_name
        self.comparisons = comparisons

    def to_attribute(self):
        """
        Render the limits to a datastar attribute to update on web client
        """
        classes = []
        for comparison in self.comparisons:
            cls = comparison["class"]
            conds = []
            op_map = dict(lt="<", gt=">=", eq="==")
            for op in op_map:
                if op in comparison:
                    conds.append(f"${self.signal_name} {op_map[op]} {comparison[op]}")
            classes.append(f"{cls}: {' && '.join(conds)}")
        result = "data-class=\"{"
        result += ", ".join(classes) + "}\""
        return result
