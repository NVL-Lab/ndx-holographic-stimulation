from importlib.resources import files
import os
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-holostim.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-holostim.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-holostim")`
OptogeneticStimulusPattern = get_class("OptogeneticStimulusPattern", "ndx-holostim")
SpiralScanning = get_class("SpiralScanning", "ndx-holostim")
TemporalFocusing = get_class("TemporalFocusing", "ndx-holostim")
PatternedOptogeneticStimulusSite = get_class("PatternedOptogeneticStimulusSite", "ndx-holostim")
PatternedOptogeneticSeries = get_class("PatternedOptogeneticSeries", "ndx-holostim")
SpatialLightModulator = get_class("SpatialLightModulator", "ndx-holostim")
LightSource = get_class("LightSource", "ndx-holostim")

# TODO: Add all classes to __all__ to make them accessible at the package level
__all__ = [
   "OptogeneticStimulusPattern", 
   "SpiralScanning",
  "TemporalFocusing", 
  "PatternedOptogeneticStimulusSite", 
  "PatternedOptogeneticSeries", 
  "SpatialLightModulator",
  "LightSource"
]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, os, __location_of_this_file, __spec_path
