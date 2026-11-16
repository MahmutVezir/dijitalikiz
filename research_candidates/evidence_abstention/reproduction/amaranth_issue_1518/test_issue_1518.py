"""Independent RTLIL string-brace escaping reproducer for Amaranth issue #1518."""
from __future__ import annotations

import unittest

from amaranth.back import rtlil
from amaranth.hdl import Module, Print


class AmaranthIssue1518Regression(unittest.TestCase):
    def test_literal_curly_braces_are_escaped_in_rtlil_format(self) -> None:
        module = Module()
        module.d.comb += [Print("{"), Print("}")]
        output = rtlil.convert(module, ports=(), emit_src=False)
        self.assertIn('parameter \\FORMAT "{{\\n"', output)
        self.assertIn('parameter \\FORMAT "}}\\n"', output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
