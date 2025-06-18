from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file
from datetime import datetime

from ndx_holostim import TemporalFocusing


class TestTemporalFocusingConstructor(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="test TemporalFocusing",
            identifier="TF123",
            session_start_time=datetime.now().astimezone(),
        )

    def test_constructor(self):
        tfocus = TemporalFocusing(
            name="tfocus1",
            description="Temporal focusing pattern",
            duration=0.8,
            number_of_stimulus_presentation=2,
            inter_stimulus_interval=0.3,
            lateral_point_spread_function="1.2 ± 0.3 µm",
            axial_point_spread_function="3.4 ± 0.5 µm"
        )

        self.assertEqual(tfocus.name, "tfocus1")
        self.assertEqual(tfocus.description, "Temporal focusing pattern")
        self.assertEqual(tfocus.duration, 0.8)
        self.assertEqual(tfocus.number_of_stimulus_presentation, 2)
        self.assertEqual(tfocus.inter_stimulus_interval, 0.3)
        self.assertEqual(tfocus.lateral_point_spread_function, "1.2 ± 0.3 µm")
        self.assertEqual(tfocus.axial_point_spread_function, "3.4 ± 0.5 µm")


class TestTemporalFocusingRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="test TemporalFocusing roundtrip",
            identifier="TF456",
            session_start_time=datetime.now().astimezone(),
        )
        self.path = "test_temporal_focusing.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        tfocus = TemporalFocusing(
            name="tfocus1",
            description="Temporal focusing pattern",
            duration=0.8,
            number_of_stimulus_presentation=2,
            inter_stimulus_interval=0.3,
            lateral_point_spread_function="1.2 ± 0.3 µm",
            axial_point_spread_function="3.4 ± 0.5 µm"
        )

        self.nwbfile.add_lab_meta_data(tfocus)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_tfocus = read_nwbfile.lab_meta_data["tfocus1"]

            self.assertContainerEqual(tfocus, read_tfocus)
