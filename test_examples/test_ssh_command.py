"""Purpose: Demonstrate a system test that executes and validates an SSH command."""

from embedded_framework.embedded_test_base import EmbeddedTestCase

class TestSshCommand(EmbeddedTestCase):
    """Purpose: Verify that an SSH DUT executes a command successfully."""

    dut_name = "ssh_dut"

    def test_uname_returns_success(self) -> None:
        # GIVEN a configured SSH DUT
        # WHEN its kernel release is requested
        self.logger.info("Executing uname -r through the SSH DUT")
        result = self.dut.execute("uname -r")
        self.logger.info("SSH command finished with exit status %s", result.exit_status)

        # THEN the command succeeds with the expected release
        self.assertEqual(result.exit_status, 0)
        self.assertEqual(result, "5.10.198")
