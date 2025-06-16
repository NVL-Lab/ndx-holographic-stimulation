from datetime import datetime
from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file

from ndx_holostim import SpatialLightModulator


class TestSpatialLightModulatorConstructor(TestCase):
    def test_constructor(self):
        slm = SpatialLightModulator(
            name="SLM-A1",
            model="Hamamatsu X13138",
            resolution=0.65
        )

        self.assertEqual(slm.name, "SLM-A1")
        self.assertEqual(slm.model, "Hamamatsu X13138")
        self.assertEqual(slm.resolution, 0.65)


class TestSpatialLightModulatorRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="SLM metadata test",
            identifier="SLM-001",
            session_start_time=datetime.now().astimezone(),
        )
        self.path = "test_spatial_light_modulator.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        slm = SpatialLightModulator(
            name="SLM-B2",
            model="Meadowlark XY-Phase",
            resolution=1.2
        )

        self.nwbfile.add_device(slm)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_slm = read_nwbfile.devices["SLM-B2"]
            self.assertContainerEqual(slm, read_slm)
