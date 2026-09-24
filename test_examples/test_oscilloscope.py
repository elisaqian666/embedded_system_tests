"""Reference tests for the configured LAN/SCPI oscilloscope."""

import os
from unittest import SkipTest

from embedded_framework.embedded_test_base import EmbeddedTestCase
from embedded_framework.instruments import Oscilloscope

class TestOscilloscopeReference(EmbeddedTestCase):
    """Use the standard system-test lifecycle for the shared oscilloscope."""

    @classmethod
    def setUpClass(cls) -> None:
        if not os.getenv("OSCILLOSCOPE_REFERENCE_HOST"):
            raise SkipTest("OSCILLOSCOPE_REFERENCE_HOST is not configured")
        super().setUpClass()
        assert isinstance(cls.oscilloscope, Oscilloscope)

    def test_oscilloscope_identify(self) -> None:
        # GIVEN a connected configured oscilloscope
        # WHEN its SCPI identity is requested
        self.oscilloscope.connect()
        response = self.oscilloscope.identify()
        self.logger.info("Oscilloscope *IDN?: %s", response)

        # THEN it returns a non-empty manufacturer/model response
        self.assertTrue(response)
