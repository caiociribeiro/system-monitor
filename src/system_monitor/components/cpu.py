import subprocess
import json
from system_monitor.core.metric import Metric

_AMD_PREFIX = "k10temp"
_AMD_CPU_MAIN_SENSOR = "Tctl"
# _AMD_CPU_ALT_SENSOR = "Tccd1"

# _INTEL_PREFIX = "coretemp"
# _INTEL_CPU_MAIN_SENSOR = "CPU Package"

class CPU:
    def __init__(self):
        self.name: str | None = None
        self.vendor: str = "Unknown"
        self.sensor: str | None = None
        self.temp: Metric = Metric("temp", "°C")
        self.clocks: list[Metric] = []
        self._detected = False

    def update(self, sensors: dict) -> None:
        if not self._detected:
            self._detect_cpu()

        if self.vendor == "AMD":
            self._update_amd(sensors)
        elif self.vendor == "Intel":
            self._update_intel(sensors)

        self._update_clock()

    def _detect_cpu(self) -> None:
        data = subprocess.check_output(["lscpu", "-J"])
        data = json.loads(data)["lscpu"]

        self.vendor = next(i["data"] for i in data if i["field"] == "Vendor ID:")
        self.name = next(i["data"] for i in data if i["field"] == "Model name:")

        if "AMD" in self.vendor:
            self.vendor = "AMD"
        elif "Intel" in self.vendor:
            self.vendor = "Intel"

        self._detected = True

    def _update_amd(self, sensors: dict) -> None:
        for key, value in sensors.items():
            if key.startswith(_AMD_PREFIX):
                self.sensor = _AMD_CPU_MAIN_SENSOR
                self.temp.update(next(iter(value[_AMD_CPU_MAIN_SENSOR].values())))
                return

    # TODO
    def _update_intel(self, sensors: dict) -> None:
        pass

    def _update_clock(self) -> None:
        clocks: list[float] = []

        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.lower().startswith("cpu mhz"):
                    clocks.append(float(line.split(":")[1].strip()))

        if not self._detected:
            for i, mhz in enumerate(clocks):
                metric = Metric(f"clock_core_{i}", "MHz")
                metric.update(mhz)
                self.clocks.append(metric)

            self._detected = True
            return

        for metric, mhz in zip(self.clocks, clocks):
            metric.update(mhz)

