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


## Additional source evidence

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

## Additional producer and configuration evidence

The muon processor contains early-return paths that store default/invalid muon containers:

```python
154:         if self.subarray.tel[tel_id].optics.n_mirrors != 1:
155:             self.log.warning(
156:                 f"Skipping non-single mirror telescope {tel_id},"
157:                 " muon-fitting for dual-mirror telescope is currently"
158:                 " not supported. Exclude dual mirror telescopes via setting"
159:                 " 'EventSource.allowed_tels'."
160:             )
161:             event.muon.tel[tel_id] = INVALID
162:             return
163: 
164:         self.log.debug(f"Processing event {event_id}, telescope {tel_id}")
165:         dl1 = event.dl1.tel[tel_id]
166:         image = dl1.image
167:         mask = dl1.image_mask
168:         if mask is None:
169:             mask = image > 0
170: 
171:         checks = self.dl1_query(dl1_params=dl1.parameters)
172: 
173:         if not all(checks):
174:             event.muon.tel[tel_id] = INVALID
175:             return
```

For an invalid ring radius, the parameter calculation returns the default parameter container:

```python
247:         if np.isnan(ring.radius.value):
248:             return INVALID_PARAMETERS
249: 
```

For a processed event, the muon processor calls the radial-light-distribution function and places its outputs into the parameter container:

```python
297:         radial_std_dev, skewness, excess_kurtosis = radial_light_distribution(
298:             ring.center_fov_lon,
299:             ring.center_fov_lat,
300:             fov_lon,
301:             fov_lat,
302:             image,
303:         )
304: 
305:         return MuonParametersContainer(
306:             containment=containment,
307:             completeness=completeness,
308:             intensity_ratio=intensity_ratio,
309:             mean_squared_error=mse,
310:             ring_intensity=ring_intensity,
311:             intensity_outside_ring=intensity_outside_ring,
312:             n_pixels_in_ring=n_pixels_in_ring,
313:             mean_intensity_outside_ring=mean_intensity_outside_ring,
314:             radial_std_dev=radial_std_dev,
315:             skewness=skewness,
316:             excess_kurtosis=excess_kurtosis,
317:         )
```

The base implementation of radial_light_distribution returns the standard deviation, skewness, and excess kurtosis:

```python
324:     if np.sum(image) == 0:
325:         return (
326:             np.nan * u.deg,
327:             np.nan * u.dimensionless_unscaled,
328:             np.nan * u.dimensionless_unscaled,
329:         )
330: 
331:     pixel_r = np.hypot(pixel_fov_lon - center_fov_lon, pixel_fov_lat - center_fov_lat)
332: 
333:     mean = np.average(pixel_r, weights=image)
334:     delta_r = pixel_r - mean
335:     radial_std_dev = np.sqrt(np.average(delta_r**2, weights=image))
336:     skewness = (
337:         np.average(delta_r**3, weights=image)
338:         / radial_std_dev**3
339:         * u.dimensionless_unscaled
340:     )
341:     excess_kurtosis = (
342:         np.average(delta_r**4, weights=image) / radial_std_dev**4 - 3.0
343:     ) * u.dimensionless_unscaled
344: 
345:     return (
346:         radial_std_dev,
347:         skewness,
348:         excess_kurtosis,
349:     )
```

The processor tool gates both muon processing and writing on the DataWriter flag:

```python
241:     def should_compute_muon_parameters(self):
242:         """returns true if we should compute muon parameters info"""
243:         if self.write.write_muon_parameters:
244:             return True
245: 
246:         return False
247: 
```

```python
305: 
306:             if self.should_compute_dl1:
307:                 self.process_images(event)
308: 
309:             if self.should_compute_muon_parameters:
310:                 self.process_muons(event)
311: 
312:             if self.should_compute_dl2:
313:                 self.process_shower(event)
314: 
315:             self.write(event)
316: 
```

The DataWriter implementation itself calls the muon-table writer only under the same flag:

```python
336:             self._write_dl2_telescope_events(event)
337:             self._write_dl2_stereo_event(event)
338: 
339:         if self.write_muon_parameters:
340:             self._write_muon_telescope_events(event)
341: 
```

This creates a configuration/provenance question to reconcile: the published report above sets the flag to False, while the reported traceback shows that the muon-table writer executed. The supplied report does not identify an effective configuration override.
