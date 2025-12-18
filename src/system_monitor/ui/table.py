from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich import box

def fmt_metric(metric: float | None, unit: str) -> str:
    if metric is None:
        return "Unknown"
    return f"{metric:6.2f}{unit}"


def build_table(cpu, nvme, ram, gpu) -> Group:
    table = Table(box=box.ASCII2, expand=False)

    table.add_column("Sensor", width=40, no_wrap=True)
    table.add_column("Current", width=15, justify="right")
    table.add_column("Min", width=15, justify="right")
    table.add_column("Max", width=15, justify="right")

    # CPU
    table.add_row(cpu.name)
    table.add_row(
        f"└─ Temp ({cpu.sensor})",
        fmt_metric(cpu.temp.current, cpu.temp.unit),
        fmt_metric(cpu.temp.min, cpu.temp.unit),
        fmt_metric(cpu.temp.max, cpu.temp.unit),
    )

    table.add_row("   Clocks")
    for i, clock in enumerate(cpu.clocks):
        table.add_row(
            f"   └─ {clock.name}" if i == 0 else f"      {clock.name}",
            fmt_metric(clock.current, f" {clock.unit}"),
            fmt_metric(clock.min, f" {clock.unit}"),
            fmt_metric(clock.max, f" {clock.unit}"),
        )

    for i in range(len(nvme.devices)):
        table.add_row()
        table.add_row(f"NVME #{i} - {nvme.devices[i].sensor}")
        table.add_row(
            "└─ Temp",
            fmt_metric(nvme.devices[i].temp.current, nvme.devices[i].temp.unit),
            fmt_metric(nvme.devices[i].temp.min, nvme.devices[i].temp.unit),
            fmt_metric(nvme.devices[i].temp.max, nvme.devices[i].temp.unit),
        )

    for i in range(len(ram.devices)):
        table.add_row()
        table.add_row(f"DIMM #{i} - {ram.devices[i].sensor}")
        table.add_row(
            "└─ Temp",
            fmt_metric(ram.devices[i].temp.current, ram.devices[i].temp.unit),
            fmt_metric(ram.devices[i].temp.min, ram.devices[i].temp.unit),
            fmt_metric(ram.devices[i].temp.max, ram.devices[i].temp.unit),
        )

    table.add_row()

    if gpu.temp is not None:
        table.add_row(gpu.name)
        table.add_row(
            "└─ Temp",
            fmt_metric(gpu.temp.current, gpu.temp.unit),
            fmt_metric(gpu.temp.min, gpu.temp.unit),
            fmt_metric(gpu.temp.max, gpu.temp.unit),
        )

    footer = Panel(
            Align.left("[bold]Ctrl+c[/bold] to quit"),
            box=box.SIMPLE,
            width=80
        )

    return Group(table, footer)
