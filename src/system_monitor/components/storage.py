import os
import subprocess
import json
from system_monitor.core.metric import Metric


class STORAGE:
    def __init__(self) -> None:
        self.devices: list[STORAGEDevice] = []
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
            name = dev["name"]
            model = dev.get("model", "Unknown")
            tran = dev.get("tran")

            if tran is None:
                continue

            devnode = f"/dev/{name}"

            device = STORAGEDevice(
                name=name,
                model=model,
                tran=tran,
                devnode=devnode,
            )

            if tran == "nvme":
                device.source = "nvme"
            else:
                device.source = "smart"

            self.devices.append(device)

        self._detected = True

    def _get_nvme_sensor_keys(self, sensors: dict) -> list[str]:
        return [k for k in sensors.keys() if k.startswith("nvme-pci")]

    def _read_smart_temp(self, devnode: str) -> float | None:
        try:
            out = subprocess.check_output(
                ["smartctl", "-A", devnode],
                text=True,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            return None

        for line in out.splitlines():
            if "Temperature_Celsius" in line or "Airflow_Temperature_Cel" in line:
                return float(line.split()[-1])

        return None

    def _update_devices(self, sensors: dict) -> None:
        nvme_sensor_keys = [k for k in sensors.keys() if k.startswith("nvme-pci")]

        for dev in self.devices:
            if dev.source == "nvme":
                if not nvme_sensor_keys:
                    continue

                try:
                    ctrl_index = int(dev.name.replace("nvme", "").split("n")[0])
                except Exception:
                    continue

                if ctrl_index >= len(nvme_sensor_keys):
                    continue

                sensor = nvme_sensor_keys[ctrl_index]
                dev.sensor = sensor

                composite = sensors[sensor].get("Composite")
                if not composite:
                    continue

                temp = next(iter(composite.values()))
                dev.temp.update(temp)

            elif dev.source == "smart":
                temp = self._read_smart_temp(dev.devnode)
                if temp is not None:
                    dev.temp.update(temp)


class STORAGEDevice:
    def __init__(self, name: str, model: str, tran: str, devnode: str) -> None:
        self.name = name
        self.model = model
        self.tran = tran
        self.devnode = devnode
        self.sensor: str | None = None
        self.source: str | None = None
        self.temp: Metric = Metric("temp", "°C")
