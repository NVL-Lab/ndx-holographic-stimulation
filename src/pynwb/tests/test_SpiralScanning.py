from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file
from datetime import datetime

from ndx_holostim import SpiralScanning


class TestSpiralScanningConstructor(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description='test SpiralScanning',
            identifier='SS123',
            session_start_time=datetime.now(),
        )

    def test_constructor(self):
        spiral = SpiralScanning(
            name='spiral1',
            description='Spiral stimulation pattern',
            duration=0.5,
            number_of_stimulus_presentation=3,
            inter_stimulus_interval=0.1,
            diameter=0.01,
            height=0.02,
            number_of_revolutions=5,
        )

        self.assertEqual(spiral.name, 'spiral1')
        self.assertEqual(spiral.description, 'Spiral stimulation pattern')
        self.assertEqual(spiral.duration, 0.5)
        self.assertEqual(spiral.number_of_stimulus_presentation, 3)
        self.assertEqual(spiral.inter_stimulus_interval, 0.1)
        self.assertEqual(spiral.diameter, 0.01)
        self.assertEqual(spiral.height, 0.02)
        self.assertEqual(spiral.number_of_revolutions, 5)


class TestSpiralScanningRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description='test SpiralScanning roundtrip',
            identifier='SS456',
            session_start_time=datetime.now(),
        )
        self.path = 'test_spiral_scanning.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        spiral = SpiralScanning(
            name='spiral1',
            description='Spiral stimulation pattern',
            duration=0.5,
            number_of_stimulus_presentation=3,
            inter_stimulus_interval=0.1,
            diameter=0.01,
            height=0.02,
            number_of_revolutions=5,
        )

        self.nwbfile.add_lab_meta_data(spiral)

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_spiral = read_nwbfile.lab_meta_data['spiral1']
            self.assertContainerEqual(spiral, read_spiral)
