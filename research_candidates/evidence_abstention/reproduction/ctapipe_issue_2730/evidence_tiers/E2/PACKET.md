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


## Additional technical source evidence

Reported execution traceback (machine-specific home paths removed; stack frames and exception text preserved from the reporter's comment):

```text
DataWriter.__call__ (datawriter.py:340)
  self._write_muon_telescope_events(event)
DataWriter._write_muon_telescope_events (datawriter.py:677)
  self._writer.write(...)
HDF5TableWriter.write (hdf5tableio.py:491)
HDF5TableWriter._append_row (hdf5tableio.py:457)
  value = self._apply_col_transform(table_name, colname, value)
TableWriter._apply_col_transform (tableio.py:199)
  value = tr(value)
QuantityColumnTransform.__call__ (tableio.py:349)
  return value.to_value(self.unit)
AttributeError: 'float' object has no attribute 'to_value'
```

Container field declarations at the pinned source revision:

```python
1213:     radial_std_dev = Field(
1214:         nan * u.deg,
1215:         "Standard deviation of the radial light distribution.",
1216:     )
1217:     skewness = Field(nan, "Skewness of the light distribution along the ring radius.")
1218:     excess_kurtosis = Field(
1219:         nan, "Excess kurtosis of the light distribution along the ring radius."
1220:     )
```

Relevant field validation logic at the pinned source revision:

```python
132:     def validate(self, value):
133:         """
134:         check that a given value is appropriate for this Field
135: 
136:         Parameters
137:         ----------
138:         value: Any
139:            the value to test
140: 
141:         Raises
142:         ------
143:         FieldValidationError:
144:             if the value is not valid
145:         """
146: 
147:         if self.allow_none and value is None:
148:             return
149: 
150:         errorstr = f"the value '{value}' ({type(value)}) is invalid: "
151: 
152:         if self.type is not None and not isinstance(value, self.type):
153:             raise FieldValidationError(
154:                 f"{errorstr} Should be an instance of {self.type}"
155:             )
156: 
157:         if isinstance(value, Container):
158:             # recursively check sub-containers
159:             value.validate()
160:             return
161: 
162:         if isinstance(value, Map):
163:             for key, map_value in value.items():
164:                 if isinstance(map_value, Container):
165:                     try:
166:                         map_value.validate()
167:                     except FieldValidationError as err:
168:                         raise FieldValidationError(f"[{key}]: {err} ")
169:             return
170: 
171:         if self.unit is not None:
172:             if not isinstance(value, Quantity):
173:                 raise FieldValidationError(
174:                     f"{errorstr} Should have units of {self.unit}"
175:                 ) from None
176:             try:
177:                 value.to(self.unit)
178:             except UnitConversionError as err:
179:                 raise FieldValidationError(f"{errorstr}: {err}")
180: 
```

HDF5 column-transform registration at the pinned source revision:

```python
294:         if isinstance(value, Quantity):
295:             unit = field.unit or value.unit
296:             tr = QuantityColumnTransform(unit=unit)
297:             value = tr(value)
298:             self.add_column_transform(table_name, name, tr)
299: 
```

HDF5 append path at the pinned source revision:

```python
442:     def _append_row(self, table_name, containers):
443:         """
444:         append a row to an already initialized table. This is called
445:         automatically by `write()`
446:         """
447:         table = self._tables[table_name]
448:         row = table.row
449: 
450:         for container in containers:
451:             selected_fields = filter(
452:                 lambda kv: kv[0] in table.colnames,
453:                 container.items(add_prefix=self.add_prefix),
454:             )
455:             for colname, value in selected_fields:
456:                 try:
457:                     value = self._apply_col_transform(table_name, colname, value)
458:                     row[colname] = value
459:                 except Exception:
460:                     self.log.error(
461:                         f"Error writing col {colname} of "
462:                         f"container {container.__class__.__name__}"
463:                     )
464:                     raise
```

Quantity transform implementation at the pinned source revision:

```python
342: class QuantityColumnTransform(ColumnTransform):
343:     """A Column Transform that transforms quantities to their values in the given unit"""
344: 
345:     def __init__(self, unit):
346:         self.unit = unit
347: 
348:     def __call__(self, value):
349:         return value.to_value(self.unit)
350: 
351:     def inverse(self, value):
352:         return Quantity(value, self.unit, copy=COPY_IF_NEEDED)
```
