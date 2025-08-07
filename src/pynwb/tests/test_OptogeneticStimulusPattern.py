from datetime import datetime
from pynwb import NWBHDF5IO
from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile

from ndx_holostim import OptogeneticStimulusPattern


class TestOptogeneticStimulusPatternConstructor(TestCase):
    """Unit test for constructing OptogeneticStimulusPattern."""

    def setUp(self):
        self.nwbfile = mock_NWBFile(
            session_description='Test session',
            identifier='test_id',
            session_start_time=datetime.now().astimezone()
        )

    def test_constructor(self):
        pattern = OptogeneticStimulusPattern(
            name='stim1',
            description='Single ROI pattern',
            duration=0.05,
            number_of_stimulus_presentation=10,
            inter_stimulus_interval=0.1
        )

        self.assertEqual(pattern.name, 'stim1')
        self.assertEqual(pattern.description, 'Single ROI pattern')
        self.assertEqual(pattern.duration, 0.05)
        self.assertEqual(pattern.number_of_stimulus_presentation, 10)
        self.assertEqual(pattern.inter_stimulus_interval, 0.1)


class TestOptogeneticStimulusPatternRoundtrip(TestCase):
    """Roundtrip test for OptogeneticStimulusPattern."""

    def setUp(self):
        self.nwbfile = mock_NWBFile(
            session_description='Test session',
            identifier='test_id',
            session_start_time=datetime.now().astimezone()  # Avoid timezone warning
        )
        self.path = 'test_optostim.nwb'  # NWB file will be saved to disk

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        pattern = OptogeneticStimulusPattern(
            name='stim1',
            description='Single ROI pattern for opsin activation',
            duration=0.05,
            number_of_stimulus_presentation=10,
            inter_stimulus_interval=0.1
        )

        self.nwbfile.add_lab_meta_data(pattern)

        # Write to file
        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        # Read back and print contents
        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_pattern = read_nwbfile.lab_meta_data['stim1']
            self.assertContainerEqual(pattern, read_pattern)
