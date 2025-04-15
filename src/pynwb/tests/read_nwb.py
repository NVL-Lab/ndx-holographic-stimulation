from ndx_holostim import OptogeneticStimulusPattern

import numpy as np
from pynwb import NWBHDF5IO

path = "ndx-holostim/src/pynwb/tests/test_optostim.nwb"

with NWBHDF5IO(path, mode='r', load_namespaces=True) as io:
    read_nwbfile = io.read()

    print("\n=== LabMetaData Contents ===")
    for name, meta in read_nwbfile.lab_meta_data.items():
        print(f"Metadata name: {name}")
        print(f"  Description: {getattr(meta, 'description', 'N/A')}")
        print(f"  Duration: {getattr(meta, 'duration', 'N/A')}")
        print(f"  Num Stimulus Presentations: {getattr(meta, 'number_of_stimulus_presentation', 'N/A')}")
        print(f"  Inter-Stimulus Interval: {getattr(meta, 'inter_stimulus_interval', 'N/A')}")

