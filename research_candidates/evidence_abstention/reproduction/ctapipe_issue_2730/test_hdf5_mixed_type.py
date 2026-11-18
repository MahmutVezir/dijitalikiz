import astropy.units as u
import numpy as np

from ctapipe.containers import MuonParametersContainer
from ctapipe.image.muon.features import radial_light_distribution
from ctapipe.io.hdf5tableio import HDF5TableWriter


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

    output = tmp_path / "muon-parameters.h5"
    with HDF5TableWriter(output, mode="w") as writer:
        writer.write("muon", calculated_parameters)
        writer.write("muon", default_parameters)
