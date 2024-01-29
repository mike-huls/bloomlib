import dataclasses
import time
import tracemalloc
import typing
from functools import wraps

from rich.console import Console
from rich.table import Table

@dataclasses.dataclass
class Timing:
    name:str
    times:[int]
    size:typing.Optional[int]

    @property
    def min(self):
        return min(self.times)
    @property
    def max(self):
        return max(self.times)
    @property
    def avg(self):
        return sum(self.times) / len(self.times)


# Timing = collections.namedtuple('Timing', ['name', 'times', 'size'])
def display_times(timings:[Timing], decimals:int=3, name:str=None) -> None:
    # _size = '\t\t' + str(size) if (size is not None) else ''
    table = Table()#title="Todo List")

    name = "Name" if name is None else name
    table.add_column(header=name, style="cyan", no_wrap=True)
    table.add_column(header="Min (ms)", justify="right", style="green")
    table.add_column(header="Max (ms)", justify="right", style="green")
    table.add_column(header="Avg (ms)", justify="right", style="green")
    table.add_column(header="%", justify="right", style="green")
    table.add_column(header="diff (ms)", justify="right", style="green")

    add_size_column = False

    largest_avg = max([t.avg for t in timings])

    timing:Timing
    for timing in timings:
        if (not add_size_column and timing.size is not None):
            table.add_column(header="Size", justify="right", style="green")

        # calculate % faster compared to slowest
        percent_faster = (timing.avg - largest_avg) / largest_avg if (timing.avg != largest_avg) else None
        diff_faster = largest_avg - timing.avg if (timing.avg != largest_avg) else None

        row = [
            timing.name,
            f"{timing.min:.{decimals}f}",
            f"{timing.max:.{decimals}f}",
            f"{timing.avg:.{decimals}f}",
            f"{percent_faster:.2%}" if percent_faster is not None else "-",
            f"{diff_faster:.{decimals}f}" if percent_faster is not None else "-",
        ]
        if (timing.size is not None):
            row.append(str(timing.size) if (timing.size is not None) else '')
        table.add_row(*row)
    console = Console()
    console.print(table)

def performance_check(func):
    """Measure performance of a function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
      tracemalloc.start()
      start_time = time.perf_counter()
      res = func(*args, **kwargs)
      duration = time.perf_counter() - start_time
      current, peak = tracemalloc.get_traced_memory()
      tracemalloc.stop()

      print(f"\nFunction:             {func.__name__} ({func.__doc__})"
            f"\nMemory usage:         {current / 10**6:.6f} MB"
            f"\nPeak memory usage:    {peak / 10**6:.6f} MB"
            f"\nDuration:             {duration:.6f} sec"
            f"\n{'-'*40}"
      )
      return res
    return wrapper

def time_function(func):
    """Measure performance of a function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
      start_time = time.perf_counter()
      res = func(*args, **kwargs)
      duration = time.perf_counter() - start_time

      print(f"\nFunction:             {func.__name__} ({func.__doc__})"
            f"\nDuration:             {duration:.6f} sec"
            f"\n{'-'*40}"
      )
      return res
    return wrapper
