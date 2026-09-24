"""Purpose: Demonstrate host-PC screenshots and PID-status checks."""

import os
import tempfile
import unittest
import logging

from pathlib import Path
from embedded_framework.basic_test_setup import BasicTestClass
from embedded_framework.helpers.he_host_pc import SystemHelper
from embedded_framework.helpers.he_network import NetworkHelper
from embedded_framework.helpers.he_file import FileHelper

class TestHostPc(BasicTestClass):
    """Purpose: Verify desktop capture and process status on the test host."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.system = SystemHelper()
        cls.network = NetworkHelper()
        cls.logger = logging.getLogger("test_case")
        cls.file = FileHelper()
        if not cls.system.is_os_windows():
            raise unittest.SkipTest("System is not window, do not support this test case")


    def test_screenshot_and_current_process_status(self) -> None:
        # GIVEN a writable test-method log directory
        with tempfile.TemporaryDirectory() as directory:
            screenshot = Path(self.test_method_log_store_folder) / "desktop.png"

            # WHEN the host desktop is captured
            result = self.system.get_screenshot(screenshot)
            self.logger.info("screenshot path is %s", result)

            # THEN the screenshot is saved as a non-empty file
            self.assertEqual(result.resolve(), screenshot.resolve())
            self.assertTrue(screenshot.is_file())
            self.assertGreater(screenshot.stat().st_size, 0)
        # WHEN the expected host process is queried
        running_status = self.system.is_process_running("Everything")
        self.logger.info("process status is %s", running_status)

        # THEN it is running
        self.assertTrue(running_status)

    def test_get_ip_address(self):
        # GIVEN the current host network configuration
        # WHEN its primary address is requested
        ip = self.network.get_host_ip()
        self.logger.info("Get the ip address successfully: %s", ip)

        # THEN a non-empty address is returned
        self.assertTrue(ip)

    # def test_get_usb_drives(self):
    #     # GIVEN a host with a removable drive
    #     # WHEN removable drives are listed
    #     usb_list = self.file.list_removable_drives()
    #     self.logger.info("usb_list == %s", usb_list)

    #     # THEN at least one drive can be inspected for ISO files
    #     self.assertTrue(usb_list)

    #     usb_file_list = self.file.read_usb_files(usb_list[0])

    #     for usb_file in usb_file_list:
    #         if usb_file.suffix.lower() == ".iso":
    #             self.logger.info("Found ISO file: %s",usb_file,)
