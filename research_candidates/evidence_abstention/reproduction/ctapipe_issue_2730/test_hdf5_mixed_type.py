import astropy.units as u
import numpy as np

from ctapipe.containers import (
    ArrayEventContainer,
    MuonParametersContainer,
    MuonTelescopeContainer,
)
from ctapipe.image.muon.features import radial_light_distribution
from ctapipe.io.datawriter import DataWriter
from ctapipe.io.hdf5tableio import HDF5TableWriter


class MuonDataWriterHarness:
    """Exercise the real DataWriter muon-table method without opening an event source."""

    def __init__(self, table_writer):
        self._writer = table_writer

    table_name = DataWriter.table_name
    _write_muon_telescope_events = DataWriter._write_muon_telescope_events


def test_calculated_then_default_muon_parameters_write_without_type_mismatch(tmp_path):
    center_x = 0.0 * u.deg
    center_y = 0.0 * u.deg
    pixel_x = np.linspace(-2, 2, 1855) * u.deg
    pixel_y = np.linspace(-2, 2, 1855) * u.deg
    image = np.ones(1855)

    radial_std_dev, skewness, excess_kurtosis = radial_light_distribution(
        center_x, center_y, pixel_x, pixel_y, image
    )

    calculated_parameters = MuonParametersContainer(
        radial_std_dev=radial_std_dev,
        skewness=skewness,
        excess_kurtosis=excess_kurtosis,
    )
    default_parameters = MuonParametersContainer()

    # The untyped, unitless Field definitions accept both Quantity and float.
    # The failure is introduced by the HDF5 column transform retained from row 1.
    calculated_parameters.validate()
    default_parameters.validate()

    first_event = ArrayEventContainer()
    first_event.index.obs_id = np.uint64(1)
    first_event.index.event_id = np.uint64(10)
    first_event.muon.tel[1] = MuonTelescopeContainer(parameters=calculated_parameters)

    later_event = ArrayEventContainer()
    later_event.index.obs_id = np.uint64(1)
    later_event.index.event_id = np.uint64(11)
    later_event.muon.tel[1] = MuonTelescopeContainer(parameters=default_parameters)

    output = tmp_path / "muon-parameters.h5"
    with HDF5TableWriter(output, mode="w", add_prefix=True) as table_writer:
        data_writer = MuonDataWriterHarness(table_writer)
        # This is the exact method called by DataWriter.__call__ when
        # write_muon_parameters is enabled.
        data_writer._write_muon_telescope_events(first_event)
        data_writer._write_muon_telescope_events(later_event)
