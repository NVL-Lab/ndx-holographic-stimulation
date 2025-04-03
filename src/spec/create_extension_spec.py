# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBLinkSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-holostim""",
        version="""0.1.0""",
        doc="""Extension to include Holographic Stimulation experiments""",
        author=[
            "Andrea",
            "Rishitesh",
        ],
        contact=[
            "nvl2@uab.edu",
        ],
    )
    ns_builder.include_namespace("core")
    
     # Optogenetic patterns group

    OptogeneticStimulusPattern = NWBGroupSpec(
        neurodata_type_def="OptogeneticStimulusPattern", 
        neurodata_type_inc="LabMetData", 
        doc="Holographic excitation single ROI",
        attributes=[NWBAttributeSpec(name="description", doc="description of the stimulus pattern", dtype="text", required=True),
                    NWBAttributeSpec(name="duration", doc="the time duration for a single stimulus, in sec", dtype="float32", required=True),
                    NWBAttributeSpec(name="number_of_stimulus_presentation", doc="number of times the patterned stimulus is presented in one time interval", dtype="int8", required=True),
                    NWBAttributeSpec(name="inter_stimulus_interval", doc="duration of the interval between each individual stimulus, in sec", dtype="float32", required=True)]
    )

    SpiralScanning = NWBGroupSpec(
        neurodata_type_def="SpiralScanning", 
        neurodata_type_inc="OptogeneticStimulusPattern", 
        doc="table of parameters defining the spiral scanning beam pattern",
        attributes=[NWBAttributeSpec(name="diameter", doc="spiral diameter of each spot, in m", dtype="float32", required=True),
                    NWBAttributeSpec(name="height", doc="spiral height of each spot, in m", dtype="float32", required=True),
                    NWBAttributeSpec(name="number_of_revolutions", doc="number of turns within a spiral", dtype="int8", required=True)]
    )

    TemporalFocusing = NWBGroupSpec(
        neurodata_type_def="TemporalFocusing", 
        neurodata_type_inc="OptogeneticStimulusPattern", 
        doc="table of parameters defining the temporal focusing beam-shaping",
        attributes=[NWBAttributeSpec(name="lateral_point_spread_function", doc="estimated lateral spatial profile or point spread function, expressed as mean [um] ± s.d [um]", dtype="text", required=True),
                    NWBAttributeSpec(name="axial_point_spread_function", doc="estimated axial spatial profile or point spread function, expressed as mean [um] ± s.d [um]", dtype="text", required=True)]
    )

    # Stimulus site
    
    PatternedOptogeneticStimulusSite = NWBGroupSpec(
        neurodata_type_def="PatternedOptogeneticStimulusSite", 
        neurodata_type_inc="OptogeneticStimulusSite", 
        doc="An extension of OptogeneticStimulusSite to include the geometrical representation for the stimulus.",
        attributes=[NWBAttributeSpec(name="effector", doc="Light-activated effector protein expressed by the targeted cell (eg. ChR2)", dtype="text", required=False)]
    )


    # Series

    PatternedOptogeneticSeries = NWBGroupSpec(
        neurodata_type_def="PatternedOptogeneticSeries", 
        neurodata_type_inc="TimeSeries", 
        doc="An extension of OptogeneticSeries to include the spatial patterns for the photostimulation.",
        attributes=[NWBAttributeSpec(name="unit", doc="SI unit of data", dtype="text", default_value="watts",required=False)],
        datasets=[NWBDatasetSpec(name="data", doc="value of each of the conditions to be met by the cursor for it to be considered hitting a target", dtype="numeric", dims=["num_times", "num_rois"], shape=([None], [None]), required=False),
                  NWBDatasetSpec(name='image_mask_roi', doc=("ROIs designated using a mask of size [width, height] (2D recording) or [width, height, depth] (3D recording), where for a given pixel a value of 1 indicates belonging to the ROI. The depth value may represent to which plane the roi belonged to"), quantity='*', dims=(('x', 'y'), ('x', 'y', 'z')), shape=([None] * 2, [None] * 3), required=False),
                  NWBDatasetSpec(name='center_rois', doc=("ROIs designated as a list specifying the pixel and radio ([x1, y1, r1], or voxel ([x1, y1, z1, r1]) of each ROI, where the items in the list are the  coordinates of the center of the ROI and the size of  the Roi given in radio size. The depth value may  represent to which plane the roi belonged to"), quantity='*', dims=(('number_rois', '3'), ('number_rois', '4')), shape=([None] * 2, [None] * 3), required=False),
                  NWBDatasetSpec(name='pixel_rois', doc=("ROIs designated as a list specifying all the pixels([x1, y1], or voxel ([x1, y1, z1]) of each ROI, where the items in the list are each of the pixels belonging to the roi"), quantity='*', dims=(('number_rois', 'number_pixels', '2'), ('number_rois', 'number_pixels', '3')), shape=([None] * 2, [None] * 3), required=False)],
        links=[NWBLinkSpec(name="site", doc="link to the patterned stimulus site", target_type="PatternedOptogeneticStimulusSite", required=True),
               NWBLinkSpec(name="stimulus_pattern", doc="link to the stimulus pattern", target_type="OptogeneticStimulusPattern", required=False),
               NWBLinkSpec(name="device", doc="link to the device used to generate the photostimulation", target_type="Device", required=True),
               NWBLinkSpec(name="spatial_light_modulator", doc="link to the spatial modulator device", target_type="SpatialLightModulator", required=False),
               NWBLinkSpec(name="light_source", doc="link to the light source", target_type="LightSource", required=False)]
    )

    # Light Modulator and Light Source devices

    SpatialLightModulator = NWBGroupSpec(
        neurodata_type_def="SpatialLightModulator", 
        neurodata_type_inc="Device", 
        doc="An extension of Device to include the Spatial Light Modulator metadata",
        attributes=[NWBAttributeSpec(name="model", doc="Model of the Spatial Light Modulator", dtype="text", required=False),
                    NWBAttributeSpec(name="resolution", doc="Resolution of the Spatial Light Modulator in um", dtype="float32", required=False)]
    )

    LightSource = NWBGroupSpec(
        neurodata_type_def="LightSource", 
        neurodata_type_inc="Device", 
        doc= "An extension of Device to include the Light Source metadata",
        attributes=[NWBAttributeSpec(name="stimulation_wavelenght", doc="stimulation wavelength in nm", dtype="float32", required=True),
                    NWBAttributeSpec(name="filter_description", doc="description of the filter", dtype="text", required=True),
                    NWBAttributeSpec(name="peak_power", doc="peak power of the stimulation in W", dtype="float32", required=False),
                    NWBAttributeSpec(name="intensity", doc="intensity of the excitation in W/m^2", dtype="float32", required=False),
                    NWBAttributeSpec(name="exposure_time", doc="exposure time of the sample", dtype="", required=False),
                    NWBAttributeSpec(name="pulse_rate", doc="pulse rate of the light source, if the light source is a pulsed laser", dtype="float32", required=False)]
        )

    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")


    # TODO: add all of your new data types to this list
    new_data_types = [OptogeneticStimulusPattern, SpiralScanning, TemporalFocusing, PatternedOptogeneticStimulusSite, PatternedOptogeneticSeries, SpatialLightModulator, LightSource]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
