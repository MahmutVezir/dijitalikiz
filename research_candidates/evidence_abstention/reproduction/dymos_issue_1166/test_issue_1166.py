"""Independent public-API reproducer for OpenMDAO/Dymos issue #1166.

The test builds a fresh one-phase Brachistochrone problem and checks the
polynomial-control default immediately after setup/run_model. It does not
import the upstream PR's modified balanced-field regression test.
"""
import numpy as np
import openmdao.api as om
import dymos as dm
from dymos.examples.brachistochrone.brachistochrone_ode import BrachistochroneODE


def test_issue_1166_polynomial_control_default_is_applied():
    problem = om.Problem(model=om.Group())
    phase = dm.Phase(
        ode_class=BrachistochroneODE,
        transcription=dm.GaussLobatto(num_segments=1, order=3),
    )
    problem.model.add_subsystem("phase0", phase)

    phase.set_time_options(fix_initial=True, duration_val=2.0)
    phase.add_state("x", rate_source="xdot", fix_initial=True, fix_final=False)
    phase.add_state("y", rate_source="ydot", fix_initial=True, fix_final=False)
    phase.add_state("v", rate_source="vdot", fix_initial=True, fix_final=False)
    phase.add_control(
        "theta",
        order=1,
        units="deg",
        lower=0.0,
        upper=180.0,
        control_type="polynomial",
        opt=True,
        val=[5.0, 15.0],
    )
    phase.add_parameter("g", units="m/s**2", opt=False, val=9.80665)

    problem.setup()
    problem.run_model()

    actual = problem.get_val("phase0.controls:theta")
    np.testing.assert_allclose(
        actual,
        np.array([[5.0], [15.0]]),
        rtol=0.0,
        atol=1e-12,
    )
