from datetime import datetime
from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file
from pynwb.file import LabMetData
from ndx_holostim import LightSource


class MockDevice:
    def __init__(self, name):
        self.name = name


class TestLightSourceConstructor(TestCase):
    def test_constructor(self):
        light_source = LightSource(
            name="Testing LightSource",
            stimulation_wavelenght=12.0,
            filter_description="test 450–490 nm",
            peak_power=1.5,
            intensity=1.26,
            exposure_time=0.15,
            pulse_rate=30.0
        )

        self.assertEqual(light_source.name, "Testing LightSource")
        self.assertEqual(light_source.stimulation_wavelenght, 12.0)
        self.assertEqual(light_source.filter_description, "test 450–490 nm")
        self.assertEqual(light_source.peak_power, 1.5)
        self.assertEqual(light_source.intensity, 1.26)
        self.assertEqual(light_source.exposure_time, 0.15)
        self.assertEqual(light_source.pulse_rate, 30.0)


class TestLightSourceRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="Light Source metadata test",
            identifier="LS-001",
            session_start_time=datetime.now(),
        )
        self.path = "test_light_source.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        light_source = LightSource(
            name="LS-Red",
            stimulation_wavelenght=635.0,
            filter_description="Longpass 600 nm",
            peak_power=2.0,
            intensity=9.35,
            exposure_time=0.28,
            pulse_rate=210.0
        )

        # Register mock device
        self.nwbfile.add_device(MockDevice("mock_device"))
        self.nwbfile.add_device(light_source)  # LightSource extends Device

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_ls = read_nwbfile.devices["LS-Red"]
            self.assertContainerEqual(light_source, read_ls)
