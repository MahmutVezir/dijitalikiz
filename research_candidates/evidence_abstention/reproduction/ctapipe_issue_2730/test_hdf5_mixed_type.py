import astropy.units as u
import numpy as np
import tables

from ctapipe.containers import (
    ArrayEventContainer,
    MuonParametersContainer,
    MuonTelescopeContainer,
)
from ctapipe.image.muon.features import radial_light_distribution
from ctapipe.io.datawriter import DataWriter
from ctapipe.io.hdf5tableio import HDF5TableWriter


class DataWriterCallHarness:
    """Run DataWriter.__call__ with unrelated writers stubbed and HDF5 real."""

    __call__ = DataWriter.__call__
    table_name = DataWriter.table_name
    _write_muon_telescope_events = DataWriter._write_muon_telescope_events

    write_r1_waveforms = False
    write_r0_waveforms = False
    write_dl2 = False
    _is_simulation = False

    def __init__(self, table_writer, write_muon_parameters):
        self._writer = table_writer
        self.write_muon_parameters = write_muon_parameters
        self._at_least_one_event = False
        self.muon_writer_calls = 0

    def _write_trigger(self, event):
        pass

    def _write_dl1_telescope_events(self, event):
        pass

    def _write_muon_telescope_events(self, event):
        self.muon_writer_calls += 1
        return DataWriter._write_muon_telescope_events(self, event)


def make_event(event_id, parameters):
    event = ArrayEventContainer()
    event.index.obs_id = np.uint64(1)
    event.index.event_id = np.uint64(event_id)
    event.muon.tel[1] = MuonTelescopeContainer(parameters=parameters)
    return event


def calculated_muon_parameters():
    center_x = 0.0 * u.deg
    center_y = 0.0 * u.deg
    pixel_x = np.linspace(-2, 2, 1855) * u.deg
    pixel_y = np.linspace(-2, 2, 1855) * u.deg
    image = np.ones(1855)

    radial_std_dev, skewness, excess_kurtosis = radial_light_distribution(
        center_x, center_y, pixel_x, pixel_y, image
    )
    return MuonParametersContainer(
        radial_std_dev=radial_std_dev,
        skewness=skewness,
        excess_kurtosis=excess_kurtosis,
    )


def test_config_false_does_not_execute_muon_writer(tmp_path):
    """The issue's published False value skips the traceback's writer path."""
    output = tmp_path / "muon-disabled.h5"
    with HDF5TableWriter(output, mode="w", add_prefix=True) as table_writer:
        writer = DataWriterCallHarness(table_writer, write_muon_parameters=False)
        writer(make_event(10, calculated_muon_parameters()))
        writer(make_event(11, MuonParametersContainer()))

        assert writer.muon_writer_calls == 0
        assert len(table_writer.h5file.root) == 0


def test_config_true_reproduces_hdf5_mixed_type_failure_and_fixed_success(tmp_path):
    """Enable the flag shown by the traceback, then write Quantity followed by float."""
    calculated = calculated_muon_parameters()
    default = MuonParametersContainer()

    # Both rows pass Container.validate() because the fields have no unit/type constraint.
    calculated.validate()
    default.validate()

    output = tmp_path / "muon-parameters.h5"
    with HDF5TableWriter(output, mode="w", add_prefix=True) as table_writer:
        writer = DataWriterCallHarness(table_writer, write_muon_parameters=True)
        writer(make_event(10, calculated))
        assert writer.muon_writer_calls == 1
        writer(make_event(11, default))
        assert writer.muon_writer_calls == 2

    with tables.open_file(output) as output_file:
        table = output_file.root.dl1.event.telescope.muon.tel_001
        assert table.nrows == 2
        assert "muonparameters_skewness" in table.colnames
        assert "muonparameters_excess_kurtosis" in table.colnames
