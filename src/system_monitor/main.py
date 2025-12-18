import time
from threading import Event
from rich.live import Live

from system_monitor import CPU, GPU, NVME, RAM, SensorProvider, build_table

REFRESH_RATE = 1.0

stop_event = Event()

def main() -> None:
    provider = SensorProvider()

    cpu = CPU()
    gpu = GPU()
    nvme = NVME()
    ram = RAM()

    try:
        with Live(refresh_per_second=4, screen=True) as live:
            while True:
                sensors = provider.read()

                cpu.update(sensors)
                nvme.update(sensors)
                ram.update(sensors)
                gpu.update()


                table = build_table(cpu, nvme, ram, gpu)
                live.update(table)

                time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()

