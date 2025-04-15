import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO, NWBFile, Device
from pynwb.testing import TestCase, remove_test_file

from ndx_holostim import PatternedOptogeneticSeries, OptogeneticStimulusPattern


class TestPatternedOptogeneticSeriesConstructor(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="Test PatternedOptogeneticSeries",
            identifier="POS123",
            session_start_time=datetime.now(),
        )

        # Add required links
        self.device = self.nwbfile.create_device(name="device1")
        self.light_source = Device(name="light_source")
        self.nwbfile.add_device(self.light_source)

        # Mock a spatial light modulator as a Device for now
        self.spatial_light_modulator = Device(name="slm1")
        self.nwbfile.add_device(self.spatial_light_modulator)

        # Add a dummy stimulus site object with required neurodata_type
        # For now using a generic LabMetaData object or a stub if custom
        self.stimulus_pattern = OptogeneticStimulusPattern(
            name="stim_pattern",
            description="test stim pattern",
            duration=0.5,
            number_of_stimulus_presentation=5,
            inter_stimulus_interval=0.2,
        )
        self.nwbfile.add_lab_meta_data(self.stimulus_pattern)

    def test_constructor(self):
        data = np.random.rand(100, 3)

        image_mask_roi = np.random.randint(0, 2, size=(64, 64))
        center_rois = np.random.rand(3, 3)
        pixel_rois = np.random.randint(0, 64, size=(3, 10, 2))

        pos = PatternedOptogeneticSeries(
            name="photostim_series",
            data=data,
            rate=10.0,
            unit="watts",
            description="Patterned photostimulation data",
            site=None,  # optional link
            device=self.device,
            light_source=self.light_source,
            spatial_light_modulator=self.spatial_light_modulator,
            stimulus_pattern=self.stimulus_pattern,
            image_mask_roi=image_mask_roi,
            center_rois=center_rois,
            pixel_rois=pixel_rois,
        )

        self.assertEqual(pos.name, "photostim_series")
        self.assertEqual(pos.unit, "watts")
        self.assertEqual(pos.description, "Patterned photostimulation data")
        np.testing.assert_array_equal(pos.data, data)
        np.testing.assert_array_equal(pos.image_mask_roi, image_mask_roi)
        np.testing.assert_array_equal(pos.center_rois, center_rois)
        np.testing.assert_array_equal(pos.pixel_rois, pixel_rois)
        self.assertEqual(pos.stimulus_pattern.name, "stim_pattern")


class TestPatternedOptogeneticSeriesRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="Roundtrip POS test",
            identifier="POS456",
            session_start_time=datetime.now(),
        )
        self.path = "test_patterned_optogenetic_series.nwb"

        self.device = self.nwbfile.create_device(name="device1")
        self.light_source = Device(name="light_source")
        self.nwbfile.add_device(self.light_source)

        self.spatial_light_modulator = Device(name="slm1")
        self.nwbfile.add_device(self.spatial_light_modulator)

        self.stimulus_pattern = OptogeneticStimulusPattern(
            name="stim_pattern",
            description="test stim pattern",
            duration=0.5,
            number_of_stimulus_presentation=5,
            inter_stimulus_interval=0.2,
        )
        self.nwbfile.add_lab_meta_data(self.stimulus_pattern)

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        data = np.random.rand(100, 3)
        image_mask_roi = np.random.randint(0, 2, size=(64, 64))
        center_rois = np.random.rand(3, 3)
        pixel_rois = np.random.randint(0, 64, size=(3, 10, 2))

        pos = PatternedOptogeneticSeries(
            name="photostim_series",
            data=data,
            rate=10.0,
            unit="watts",
            description="Patterned photostimulation data",
            site=None,
            device=self.device,
            light_source=self.light_source,
            spatial_light_modulator=self.spatial_light_modulator,
            stimulus_pattern=self.stimulus_pattern,
            image_mask_roi=image_mask_roi,
            center_rois=center_rois,
            pixel_rois=pixel_rois,
        )

        self.nwbfile.add_acquisition(pos)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_pos = read_nwbfile.acquisition["photostim_series"]
            self.assertContainerEqual(pos, read_pos)
