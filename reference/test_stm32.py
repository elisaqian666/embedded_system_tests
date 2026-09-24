"""STM32F407 serial reference tests using the standard system-test lifecycle."""

import os
from unittest import SkipTest

from embedded_framework.communication.serial import SerialTransport
from embedded_framework.devices import Capability
from embedded_framework.devices.mcu import Stm32Device
from embedded_framework.embedded_test_base import EmbeddedTestCase

class TestStm32Reference(EmbeddedTestCase):
    dut_name = "serial_dut"

    @classmethod
    def setUpClass(cls) -> None:
        if "STM32_REFERENCE_PORT" not in os.environ:
            raise SkipTest("STM32_REFERENCE_PORT is not configured")
        super().setUpClass()
        assert isinstance(cls.dut, Stm32Device)
        assert cls.dut.supports(Capability.SERIAL)

    def setUp(self) -> None:
        super().setUp()
        self.transport = self.dut.serial()

    def test_stm32_device_wiring(self) -> None:
        # GIVEN the configured STM32 serial transport
        # WHEN its serial settings are inspected
        # THEN they match the shared test configuration
        self.assertIsInstance(self.transport, SerialTransport)
        self.assertEqual(self.transport.port, os.environ["STM32_REFERENCE_PORT"])
        self.assertEqual(self.transport.baudrate, 115200)
        self.assertEqual(self.transport.serial_object.bytesize, 8)
        self.assertEqual(self.transport.serial_object.parity, "N")

    def test_stm32_serial_connection(self) -> None:
        # GIVEN a Runtime-owned STM32 serial transport
        # WHEN the test starts
        # THEN the transport is already connected
        self.logger.info("Verify if the Serial Transport is connected...")
        self.assertTrue(self.transport.is_connected)

    def test_stm32_uart_receive(self) -> None:
        # GIVEN an STM32 continuously transmitting UART output
        # WHEN ten serial chunks are read
        for line_number in range(1, 11):
            data = self.transport.read(256)
            self.logger.info("STM32 UART %02d: %r", line_number, data)

            # THEN each chunk contains data
            self.assertTrue(data, f"STM32 did not send UART data for line {line_number} within 3 seconds")
