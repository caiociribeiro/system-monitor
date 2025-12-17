import subprocess
import json

class SensorProvider:
    def read(self) -> dict:
        data = subprocess.check_output(["sensors", "-j"])
        return json.loads(data)
