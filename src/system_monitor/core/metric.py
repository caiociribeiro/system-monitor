class Metric:
    def __init__(self, name: str, unit: str):
        self.name: str = name
        self.unit: str = unit
        self.current: float | None = None
        self.min: float | None = None
        self.max: float | None = None

    def update(self, value: float) -> None:
        self.current = value
        self.min = value if self.min is None else min(self.min, value)
        self.max = value if self.max is None else max(self.max, value)
