# Software bug report

DataWriter: Caught unexpected exception: 'float' object has no attribute 'to_value'

**Describe the bug**
Looks like we can not write the muonparameters_skewness during the muon analysis 
Error writing col muonparameters_skewness of container MuonParametersContainer

**To Reproduce**
```
ctapipe-process --overwrite --input=$in_simtel_file --output=$out_r0_dl1_h5_file --config=$config_file
```

$config_file:
```yaml
DataWriter:
  output_path: None
  write_muon_parameters: False
  write_dl1_parameters: False
  write_dl1_images: True
  overwrite: True

MuonProcessor:
  completeness_threshold: 30
  ratio_width: 1.5
  pedestal: 1.1

MuonIntensityFitter:
  hole_radius_m: [["type", "LST_*", 0.308]]
  spe_width: 0.5
  min_lambda_m: 0.0000003
  max_lambda_m: 0.0000006
  oversampling: 3

ImageParameterQuery:
  quality_criteria: [
      ["min_pixels", "dl1_params.morphology.n_pixels > 100"],
      ["min_intensity", "dl1_params.hillas.intensity > 500"]
    ]

RingQuery:
  quality_criteria: [
      ["radius_not_nan", "np.isfinite(ring.radius.value)"],
      ["min_pixels", "np.count_nonzero(mask) > 50"],
      ["ring_containment", "parameters.containment > 0.5"]
    ]

ImageProcessor:
  image_cleaner_type: "TailcutsImageCleaner"
  use_telescope_frame: True
  apply_image_modifier: False

TailcutsImageCleaner:
  picture_threshold_pe : 10
  boundary_threshold_pe : 5
  min_picture_neighbors :  2
  keep_isolated_pixels : False

TimeConstrainedImageCleaner:
  time_limit_core_ns: 4.5
  time_limit_boundary_ns: 1.5

ImageQualityQuery:
  quality_criteria: [["size_greater_0", "image.sum() > 0"]]

CameraCalibrator:
  data_volume_reducer_type: "NullDataVolumeReducer"
  image_extractor_type: "GlobalPeakWindowSum"
  invalid_pixel_handler_type: "NeighborAverage"
  apply_waveform_time_shift: False
  apply_peak_time_shift: True

GlobalPeakWindowSum:
  window_width: 7
  window_shift: 3
  apply_integration_correction: True
  pixel_fraction: 1
```



**Expected behavior**
normal operation with output file together with muon parameters 

