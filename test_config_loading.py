from pathlib import Path
import runpy

from embedded_framework.configurator.configurator_dut import load_mapping


def test_shared_configuration_loads_multiple_duts(monkeypatch) -> None:
    monkeypatch.setenv("STM32_REFERENCE_PORT", "COM1")
    path = Path(__file__).parents[1] / "config" / "test_config.py"
    config = runpy.run_path(path)["config"]
    framework_config = load_mapping(config, source=path)
    assert set(framework_config.devices) == {"http_dut", "ssh_dut", "serial_dut"}
