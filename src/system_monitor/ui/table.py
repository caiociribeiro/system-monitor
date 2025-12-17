from rich.table import Table

CELSIUS = "°C"
SEPARATOR = "-" * 10



def fmt_metric(metric: float | None, unit: str) -> str:
    if metric is None:
        return "Unknown"
    return f"{metric:6.2f}{unit}"


def build_table(cpu, nvme, ram, gpu) -> Table:
    table = Table(expand=False)

    table.add_column("Sensor", width=40, no_wrap=True)
    table.add_column("Current", width=10, justify="right")
    table.add_column("Min", width=10, justify="right")
    table.add_column("Max", width=10, justify="right")

    # CPU
    table.add_row(cpu.name, SEPARATOR, SEPARATOR, SEPARATOR)
    table.add_row(
        f"└─ Temp ({cpu.sensor})",
        fmt_metric(cpu.temp.current, cpu.temp.unit),
        fmt_metric(cpu.temp.min, cpu.temp.unit),
        fmt_metric(cpu.temp.max, cpu.temp.unit),
    )

    for i in range(len(nvme.devices)):
        table.add_row()
        table.add_row(f"NVME #{i} - {nvme.devices[i].sensor}", SEPARATOR, SEPARATOR, SEPARATOR)
        table.add_row(
            "└─ Temp",
            fmt_metric(nvme.devices[i].temp.current, nvme.devices[i].temp.unit),
            fmt_metric(nvme.devices[i].temp.min, nvme.devices[i].temp.unit),
            fmt_metric(nvme.devices[i].temp.max, nvme.devices[i].temp.unit),
        )

    for i in range(len(ram.devices)):
        table.add_row()
        table.add_row(f"DIMM #{i} - {ram.devices[i].sensor}", SEPARATOR, SEPARATOR, SEPARATOR)
        table.add_row(
            "└─ Temp",
            fmt_metric(ram.devices[i].temp.current, ram.devices[i].temp.unit),
            fmt_metric(ram.devices[i].temp.min, ram.devices[i].temp.unit),
            fmt_metric(ram.devices[i].temp.max, ram.devices[i].temp.unit),
        )

    table.add_row()

    if gpu.temp is not None:
        table.add_row(gpu.name, SEPARATOR, SEPARATOR, SEPARATOR)
        table.add_row(
            "└─ Temp",
            fmt_metric(gpu.temp.current, gpu.temp.unit),
            fmt_metric(gpu.temp.min, gpu.temp.unit),
            fmt_metric(gpu.temp.max, gpu.temp.unit),
        )

    return table
