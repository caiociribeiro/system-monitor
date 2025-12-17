import subprocess
import json
from system_monitor.core.metric import Metric


class NVME:
    def __init__(self) -> None:
        self.devices: list[NVMEDevice] = []
        self._detected = False

    def update(self, sensors: dict) -> None:
        if not self._detected:
            self._detect_devices()
        self._update_devices(sensors)



    def _detect_devices(self) -> None:
        data = subprocess.check_output(
            ["lsblk", "-J", "-d", "-o", "NAME,MODEL,TRAN"]
        )
        devices = json.loads(data)["blockdevices"]

        for dev in devices:
            if dev["tran"] == "nvme":
                self.devices.append(
                    NVMEDevice(
                        name=dev["name"],
                        model=dev["model"],
                    )
                )

        self._detected = True

    def _update_devices(self, sensors: dict) -> None:
        for key, value in sensors.items():
            if not key.startswith("nvme"):
                continue

            temp = next(iter(value["Composite"].values()))

            # match by order of appearance ONCE
            for dev in self.devices:
                if dev.sensor is None:
                    dev.sensor = key
                    break

            for dev in self.devices:
                if dev.sensor == key:
                    dev.temp.update(temp)


class NVMEDevice:
    def __init__(self, name: str, model: str, sensor: str | None = None) -> None:
        self.name = name
        self.model = model
        self.sensor = sensor

        self.temp: Metric = Metric("temp", "°C")

