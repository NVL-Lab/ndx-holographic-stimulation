import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing import TestCase, remove_test_file

from ndx_holostim import PatternedOptogeneticSeries, OptogeneticStimulusPattern, LightSource, SpatialLightModulator, PatternedOptogeneticStimulusSite


class TestPatternedOptogeneticSeriesConstructor(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="Test PatternedOptogeneticSeries",
            identifier="POS123",
            session_start_time=datetime.now().astimezone(),
        )

        # Add device
        self.device = self.nwbfile.create_device(name="device1")
        
        #Add Light source
        self.light_source = LightSource(
            name="Testing LightSource",
            stimulation_wavelenght=12.0,
            filter_description="test 450–490 nm",
            peak_power=1.5,
            intensity=1.26,
            exposure_time=0.15,
            pulse_rate=30.0
            )
        self.nwbfile.add_device(self.light_source)

        # Add spatial light modulator
        self.spatial_light_modulator = SpatialLightModulator(
            name="SLM-A1",
            model="Hamamatsu X13138",
            resolution=0.65
            )
        self.nwbfile.add_device(self.spatial_light_modulator)

        #Add stimulus pattern
        self.stimulus_pattern = OptogeneticStimulusPattern(
            name="stim_pattern",
            description="test stim pattern",
            duration=0.5,
            number_of_stimulus_presentation=5,
            inter_stimulus_interval=0.2,
        )

        self.nwbfile.add_lab_meta_data(self.stimulus_pattern)
        
        #Add stimulus site
        self.site = PatternedOptogeneticStimulusSite(
                name="test site",
                device=self.device,
                description="test site for PatternedOptogeneticSeries testing",
                excitation_lambda=840.0,
                location="location of the test stimulus site",
                effector="test effector for stimulus site"
            )
        self.nwbfile.add_ogen_site(self.site)

    def test_constructor(self):
        image_mask_roi=np.ones((4, 4))
        center_rois=np.ones((4, 5, 6, 7))
        pixel_rois=np.ones((4, 5, 6))

        pos = PatternedOptogeneticSeries(
            name="photostim series",
            rate=10.0,
            unit="watts",
            description="Patterned photostimulation data",
            site=self.site,
            device=self.device,
            light_source=self.light_source,
            spatial_light_modulator=self.spatial_light_modulator,
            stimulus_pattern=self.stimulus_pattern,
            image_mask_roi=image_mask_roi,
            center_rois=center_rois,
            pixel_rois=pixel_rois,
        )

        self.assertEqual(pos.name, "photostim series")
        self.assertEqual(pos.rate, 10.0)
        self.assertEqual(pos.unit, "watts")
        self.assertEqual(pos.description, "Patterned photostimulation data")
        np.testing.assert_array_equal(pos.image_mask_roi, image_mask_roi)
        np.testing.assert_array_equal(pos.center_rois, center_rois)
        np.testing.assert_array_equal(pos.pixel_rois, pixel_rois)
        self.assertContainerEqual(pos.stimulus_pattern, self.stimulus_pattern)
        self.assertContainerEqual(pos.spatial_light_modulator, self.spatial_light_modulator)
        self.assertContainerEqual(pos.light_source, self.light_source)
        self.assertContainerEqual(pos.site, self.site)



class TestPatternedOptogeneticSeriesRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="Roundtrip POS test",
            identifier="POS456",
            session_start_time=datetime.now().astimezone(),
        )
        self.path = "test_patterned_optogenetic_series.nwb"
        #Repeating the same steps as the constructor and adding to nwb file   
        self.device = self.nwbfile.create_device(name="device1")
        self.light_source = LightSource(
            name="Testing LightSource",
            stimulation_wavelenght=12.0,
            filter_description="test 450–490 nm",
            peak_power=1.5,
            intensity=1.26,
            exposure_time=0.15,
            pulse_rate=30.0
            )
        self.nwbfile.add_device(self.light_source)

        self.spatial_light_modulator = SpatialLightModulator(
            name="SLM-A1",
            model="Hamamatsu X13138",
            resolution=0.65
            )
        self.nwbfile.add_device(self.spatial_light_modulator)

        self.stimulus_pattern = OptogeneticStimulusPattern(
            name="stim_pattern",
            description="test stim pattern",
            duration=0.5,
            number_of_stimulus_presentation=5,
            inter_stimulus_interval=0.2,
        )
        self.nwbfile.add_lab_meta_data(self.stimulus_pattern)
        
        self.site = PatternedOptogeneticStimulusSite(
                name="test site",
                device=self.device,
                description="test site for PatternedOptogeneticSeries testing",
                excitation_lambda=840.0,
                location="location of the test stimulus site",
                effector="test effector for stimulus site"
            )
        self.nwbfile.add_ogen_site(self.site)

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        image_mask_roi=np.ones((4, 4))
        center_rois=np.ones((4, 5, 6, 7))
        pixel_rois=np.ones((4, 5, 6))

        pos = PatternedOptogeneticSeries(
            name="photostim_series",
            rate=10.0,
            unit="watts",
            description="Patterned photostimulation data",
            site=self.site,
            device=self.device,
            light_source=self.light_source,
            spatial_light_modulator=self.spatial_light_modulator,
            stimulus_pattern=self.stimulus_pattern,
            image_mask_roi=image_mask_roi,
            center_rois=center_rois,
            pixel_rois=pixel_rois,
        )

        self.nwbfile.add_acquisition(pos)
        #Write and read NWB file
        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_pos = read_nwbfile.acquisition["photostim_series"]
            self.assertContainerEqual(pos, read_pos)
