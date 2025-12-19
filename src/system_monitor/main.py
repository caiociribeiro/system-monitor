import time
from threading import Event
from rich.live import Live

from system_monitor import CPU, GPU, STORAGE, RAM, SensorProvider, build_table

REFRESH_RATE = 1.0

stop_event = Event()

def main() -> None:
    provider = SensorProvider()

    cpu = CPU()
    gpu = GPU()
    storage = STORAGE()
    ram = RAM()

    try:
        with Live(refresh_per_second=4, screen=True) as live:
            while True:
                sensors = provider.read()

                cpu.update(sensors)
                storage.update(sensors)
                ram.update(sensors)
                gpu.update()


                table = build_table(cpu, storage, ram, gpu)
                live.update(table)

                time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()

