import subprocess
from system_monitor.core.metric import Metric

# TODO: add support for intel and AMD

class GPU:
    def __init__(self) -> None:
        self.manufacturer: str = "Unknown"
        self.name: str | None = None
        self.temp: Metric = Metric("temp", "°C")
        self._detected: bool = False

    def update(self) -> None:
        if not self._detected:
            self._detect_gpu()

        match self.manufacturer:
            case "NVIDIA": self._update_nvidia()
            case _: return

    def _detect_gpu(self) -> None:
        lspci = subprocess.Popen(["lspci"], stdout=subprocess.PIPE, text=True)
        vga = subprocess.Popen(["grep", "-i", "vga"], stdin=lspci.stdout, stdout=subprocess.PIPE, text=True)

        output = vga.communicate()[0].upper()

        if "NVIDIA" in output:
            self.manufacturer = "NVIDIA"
        elif "INTEL" in output:
            self.manufacturer = "INTEL"
        elif "AMD" in output:
            self.manufacturer = "AMD"

        self._detected = True

    def _update_nvidia(self) -> None:
        data = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=" + ",".join(["name", "temperature.gpu"]), 
                "--format=csv,noheader,nounits"
            ],
            capture_output=True, 
            text=True, 
            check=True
        ).stdout.strip()

        name, temp_str = data.split(", ")
        temp = float(temp_str)

        if self.name is None:
            self.name = name

        self.temp.update(temp)


        
