"""Minimal synthetic regression for NAPALM issue #2151.

This deliberately does not copy the upstream PR's Cisco device fixture.
Only the two parser-relevant NX-OS version lines are supplied; all other
command responses are empty synthetic values.
"""

from unittest.mock import patch

from napalm.nxos_ssh.nxos_ssh import NXOSSSHDriver


def test_get_facts_parses_primary_nxos_version_line():
    driver = object.__new__(NXOSSSHDriver)
    responses = {
        "show version": (
            "NXOS: version 10.3(5) [Maintenance Release]\n"
            "Host NXOS: version 10.3(5)\n"
        ),
        "show hosts": "",
        "show interface status": "",
        "show hostname": "switch-synthetic",
    }

    with (
        patch.object(driver, "_send_command", side_effect=lambda command: responses[command]),
        patch.object(driver, "_get_command_table", return_value=[]),
    ):
        facts = driver.get_facts()

    assert facts["os_version"] == "10.3(5)"
