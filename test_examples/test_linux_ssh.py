"""Reference tests for the configured Linux target reached through SSH."""

from embedded_framework.devices import Capability
from embedded_framework.embedded_test_base import EmbeddedTestCase
from embedded_framework.helpers.he_shell import CommandResult


class TestLinuxSshReference(EmbeddedTestCase):
    """Exercise the Linux device adapter using only shared test configuration."""

    dut_name = "ssh_dut"
    required_capabilities = (Capability.SHELL,)
    engine_name = "ssh"

    def setUp(self):
        super().setUp()
        self.assertTrue(self.engine.is_connected)

    def test_linux_shell_reads_os_release(self) -> None:
        # GIVEN a connected Linux shell
        # WHEN its OS release file is read
        os_release = self.dut.shell().read_text("/etc/os-release")
        self.logger.info("Linux OS release: %s", os_release.splitlines()[0])

        # THEN the device identifies an operating-system distribution
        self.assertTrue("ID=" in os_release)

    def test_linux_shell_checks_standard_paths(self) -> None:
        # GIVEN a connected Linux shell
        shell = self.dut.shell()

        # WHEN standard Linux paths are checked
        # THEN each expected path exists with its expected kind
        self.assertTrue(shell.exists_file("/etc/os-release"))
        self.assertTrue(shell.exists_dir("/tmp"))
        self.assertTrue(shell.exists("/proc"))

    def test_linux_shell_reads_memory(self) -> None:
        # GIVEN a connected Linux shell
        shell = self.dut.shell()

        # WHEN memory values are read from /proc/meminfo
        total_kb = shell.get_total_memory()
        available_kb = shell.get_available_memory()
        free_kb = shell.get_free_memory()
        self.logger.info("Linux memory: total=%d KiB available=%d KiB free=%d KiB", total_kb, available_kb, free_kb)

        # THEN the values are within the total memory range
        self.assertTrue(total_kb > 0)
        self.assertTrue(0 <= available_kb <= total_kb)
        self.assertTrue(0 <= free_kb <= total_kb)

    def test_linux_shell_reads_pid_one_memory(self) -> None:
        # GIVEN a connected Linux shell
        # WHEN PID 1 memory usage is read
        # THEN it reports a positive resident-memory value
        self.assertTrue(self.dut.shell().get_process_memory(1) > 0)

    def test_linux_command_exit_status(self) -> None:
        # GIVEN a connected Linux command engine
        # WHEN successful and unsuccessful commands are executed
        # THEN their exit statuses distinguish success from failure
        self.assertEqual(self.dut.execute("true").exit_status, 0)
        self.assertNotEqual(self.dut.execute("false", check=False).exit_status, 0)

    def test_linux_service_status(self) -> None:
        # GIVEN a service configured for this Linux DUT
        service = self.dut.config.metadata.get("service")
        if not isinstance(service, str) or not service:
            self.skipTest("Configure devices.ssh_dut.metadata.service to test service status")

        # WHEN its status is requested
        result = self.dut.service(service, "status")
        self.logger.info("systemctl status %s exited with %s", service, result.exit_status)

        # THEN command execution returns a normalized result
        self.assertIsInstance(result, CommandResult)
