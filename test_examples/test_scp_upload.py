"""Purpose: Demonstrate SCP upload to an SSH DUT."""

from pathlib import Path

from embedded_framework.embedded_test_base import EmbeddedTestCase
import logging

class TestScpUpload(EmbeddedTestCase):
    """Purpose: Upload and verify a test file in the DUT /store directory."""

    dut_name = "ssh_dut"

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.logger = logging.getLogger("test_case")

    def test_upload_example_file(self) -> None:
        # GIVEN a local example file and a configured SSH DUT
        source = Path(__file__).with_name("example1.txt")
        destination_directory = "/store"
        destination = f"{destination_directory}/{source.name}"

        # WHEN the destination is prepared and the file is uploaded through SCP
        self.logger.info("Creating remote directory %s", destination_directory)
        self.dut.execute(f"mkdir -p {destination_directory}")
        self.logger.info("Uploading %s to %s through SCP", source, destination)
        self.dut.engine().put_files(str(source), destination)

        result = self.dut.execute(f"cat {destination}")

        # THEN the remote file content equals the local source
        self.assertEqual(result.exit_status, 0)
        self.assertEqual(result.stdout, source.read_text(encoding="utf-8"))
