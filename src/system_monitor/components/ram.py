from system_monitor.core.metric import Metric

class RAM:
    def __init__(self) -> None:
        self.devices: list[RAMDevice] = []
        self._detected: bool = False

    def update(self, sensors: dict) -> None:
        if not self._detected:
            self._detect_devices(sensors)

        self._update_devices(sensors)

    def _detect_devices(self, sensors: dict) -> None:
        for key in sensors:
            if key.startswith("jc42"):
                self.devices.append(
                    RAMDevice(
                        name="DIMM",
                        model="RAM",
                        sensor=key,
                    )
                )

        self._detected = True

    def _update_devices(self, sensors: dict) -> None:
        for dev in self.devices:
            data = sensors.get(dev.sensor)
            if not data:
                continue

            temp = next(iter(data["temp1"].values()))
            dev.temp.update(temp)


class RAMDevice:
    def __init__(self, name: str, model: str, sensor: str) -> None:
        # TODO: implement method to get actual RAM info (size, manufacturer?)
        self.name = name
        self.model = model
        self.sensor = sensor

        self.temp: Metric = Metric("temp", "°C")

